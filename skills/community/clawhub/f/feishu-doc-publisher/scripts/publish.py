#!/usr/bin/env python3
import os
import sys
import argparse
import time
import re
from pathlib import Path
import feishu_api
import local_file

def load_env_file(file_path):
    if local_file.file_exists(file_path):
        with open(local_file.resolve_path(file_path), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'): continue
                parts = line.split('=', 1)
                if len(parts) == 2:
                    key, val = parts[0].strip(), parts[1].strip().strip("'\"")
                    if key not in os.environ:
                        os.environ[key] = val
        print(f"🔑 已加载配置: {file_path}")

# 环境变量加载 (由于 load_env_file 是如果不存则添加，所以最先加载的优先级最高)
# 优先级: 系统环境变量 > ~/.openclaw/.env > ~/.config/feishu-doc-publisher/.env > skill 目录/.env

OPENCLAW_ENV_PATH = os.path.join(str(Path.home()), '.openclaw', '.env')
load_env_file(OPENCLAW_ENV_PATH)

GLOBAL_CONFIG_DIR = os.path.join(str(Path.home()), '.config', 'feishu-doc-publisher')
GLOBAL_ENV_PATH = os.path.join(GLOBAL_CONFIG_DIR, '.env')
load_env_file(GLOBAL_ENV_PATH)

SKILL_DIR_ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_env_file(SKILL_DIR_ENV_PATH)

PARENT_DIR_ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env')
load_env_file(PARENT_DIR_ENV_PATH)

CURRENT_DIR_ENV_PATH = os.path.join(os.getcwd(), '.env')
if CURRENT_DIR_ENV_PATH not in [SKILL_DIR_ENV_PATH, PARENT_DIR_ENV_PATH, GLOBAL_ENV_PATH, OPENCLAW_ENV_PATH]:
    load_env_file(CURRENT_DIR_ENV_PATH)

FEISHU_APP_ID = os.environ.get('FEISHU_APP_ID')
FEISHU_APP_SECRET = os.environ.get('FEISHU_APP_SECRET')

if not FEISHU_APP_ID or not FEISHU_APP_SECRET:
    print("❌ 缺少环境变量 FEISHU_APP_ID 或 FEISHU_APP_SECRET")
    sys.exit(1)

# 参数解析
parser = argparse.ArgumentParser(description="飞书文档发布脚本")
parser.add_argument("file", help="待发布的 Markdown 文件")
parser.add_argument("--title", help="自定义文档标题")
parser.add_argument("--folder", default="", help="飞书文件夹 Token")
parser.add_argument("--share", choices=["public-read", "public-edit", "tenant-read", "tenant-edit"], help="设置公开链接或组织内权限")
parser.add_argument("--owner", help="发布后将所有权转移给指定用户。格式为 type:id (如 email:test@xx.com 或 openid:ou_xx)")
args = parser.parse_args()

file_path = local_file.resolve_path(args.file)
if not local_file.file_exists(file_path):
    print(f"❌ 文件不存在: {file_path}")
    sys.exit(1)

# 表格重建
_id_seq = 0
def short_id(prefix):
    global _id_seq
    _id_seq += 1
    return f"{prefix}_{_id_seq}"

def clean_text_element(elem):
    if 'text_run' not in elem: return elem
    result = {'text_run': {'content': elem['text_run']['content']}}
    style = elem['text_run'].get('text_element_style')
    if style:
        s = {}
        for k in ['bold', 'italic', 'strikethrough', 'underline', 'inline_code', 'link']:
            if style.get(k): s[k] = style[k]
        if s:
            result['text_run']['text_element_style'] = s
    return result

def rebuild_table_for_descendant(table_block, block_map):
    table_id = short_id('tbl')
    descendants = []
    
    prop = table_block.get('table', {}).get('property', {})
    row_size = prop.get('row_size', 0)
    col_size = prop.get('column_size', 0)
    
    table_property = {'row_size': row_size, 'column_size': col_size}
    
    # 飞书文档默认视口宽度为 820px，如果多列均分，保证最小列宽限制为 200px
    if col_size > 0:
        PAGE_WIDTH = 820
        MIN_COL_WIDTH = 200
        col_width = max(PAGE_WIDTH // col_size, MIN_COL_WIDTH)
        table_property['column_width'] = [col_width] * col_size
    
    new_table_block = {
        'block_id': table_id,
        'block_type': 31,
        'table': {'property': table_property},
        'children': []
    }
    
    cell_ids = table_block.get('children', [])
    for orig_cell_id in cell_ids:
        new_cell_id = short_id('cel')
        new_table_block['children'].append(new_cell_id)
        
        orig_cell = block_map.get(orig_cell_id)
        cell_text_blocks = []
        
        if orig_cell and 'children' in orig_cell:
            for text_block_id in orig_cell['children']:
                orig_text = block_map.get(text_block_id)
                if orig_text:
                    new_text_id = short_id('txt')
                    cell_text_blocks.append(new_text_id)
                    
                    text_block = {'block_id': new_text_id, 'block_type': orig_text['block_type']}
                    
                    type_field_map = {
                        2: 'text', 12: 'bullet', 13: 'ordered', 17: 'todo', 15: 'quote'
                    }
                    field_name = type_field_map.get(orig_text['block_type'])
                    
                    if field_name and field_name in orig_text:
                        text_block[field_name] = {
                            'elements': [clean_text_element(e) for e in orig_text[field_name].get('elements', [])]
                        }
                    else:
                        text_block['block_type'] = 2
                        text_block['text'] = {'elements': [{'text_run': {'content': ''}}]}
                    
                    descendants.append(text_block)
                    
        if not cell_text_blocks:
            empty_id = short_id('txt')
            cell_text_blocks.append(empty_id)
            descendants.append({
                'block_id': empty_id,
                'block_type': 2,
                'text': {'elements': [{'text_run': {'content': ''}}]}
            })
            
        descendants.append({
            'block_id': new_cell_id,
            'block_type': 32,
            'table_cell': {},
            'children': cell_text_blocks
        })
        
    descendants.insert(0, new_table_block)
    return {'children_id': [table_id], 'descendants': descendants}

def clean_block_for_children(block):
    cleaned = block.copy()
    cleaned.pop('parent_id', None)
    cleaned.pop('block_id', None)
    return cleaned

def table_to_text_blocks(table_block, block_map):
    cell_ids = table_block.get('children', [])
    col_size = table_block.get('table', {}).get('property', {}).get('column_size', 1)
    
    rows = []
    current_row = []
    
    for cell_id in cell_ids:
        cell = block_map.get(cell_id)
        cell_text = ''
        if cell and 'children' in cell:
            for text_id in cell['children']:
                tb = block_map.get(text_id)
                if tb and 'text' in tb and 'elements' in tb['text']:
                    for e in tb['text']['elements']:
                        if 'text_run' in e:
                            cell_text += e['text_run'].get('content', '')
        current_row.append(cell_text)
        if len(current_row) == col_size:
            rows.append(current_row)
            current_row = []
            
    return [
        {
            'block_type': 2,
            'text': {'elements': [{'text_run': {'content': ' | '.join(row)}}]}
        }
        for row in rows
    ]

def main():
    md_content = local_file.read_markdown_content(file_path)
    file_basename = os.path.basename(file_path)
    print(f"📄 读取文件: {file_basename} ({len(md_content)} 字符)")
    
    title_match = re.search(r'^#\s+(.*)', md_content, re.MULTILINE)
    title = args.title or (title_match.group(1).strip() if title_match else os.path.splitext(file_basename)[0])
    body_content = re.sub(r'^#\s+.*\n*', '', md_content, count=1)
    print(f"📝 文档标题: {title}")
    
    token = feishu_api.get_tenant_access_token(FEISHU_APP_ID, FEISHU_APP_SECRET)
    print("✅ 获取 tenant_access_token 成功")
    
    print("🔄 转换 Markdown...")
    convert_data = feishu_api.convert_markdown_to_blocks(token, body_content)
    blocks = convert_data.get('blocks', [])
    first_level_block_ids = convert_data.get('first_level_block_ids', [])
    print(f"✅ 转换成功: {len(blocks)} 个 block, {len(first_level_block_ids)} 个顶层块")
    
    block_map = {b['block_id']: b for b in blocks}
    
    image_url_map = {}
    for item in convert_data.get('block_id_to_image_urls', []):
        image_url_map[item['block_id']] = item['image_url']
        
    table_count = sum(1 for id in first_level_block_ids if block_map.get(id, {}).get('block_type') == 31)
    print(f"📋 包含 {table_count} 个表格")
    
    document_id = feishu_api.create_document(token, title, args.folder)
    print(f"✅ 文档创建成功: {document_id}")
    
    if args.share:
        print(f"⚙️ 正在配置公共权限: {args.share} ...")
        share_map = {
            "public-read": "anyone_readable",
            "public-edit": "anyone_editable",
            "tenant-read": "tenant_readable",
            "tenant-edit": "tenant_editable"
        }
        share_type = share_map.get(args.share)
        try:
            feishu_api.update_public_permission(token, document_id, share_type)
            print(f"✅ 公共权限配置成功 ({args.share})")
        except Exception as e:
            print(f"⚠️ 公共权限配置失败: {e}")
            
    owner_arg = args.owner
    if not owner_arg:
        admin_val = os.environ.get('FEISHU_ADMIN')
        if admin_val:
            if '@' in admin_val:
                owner_arg = f"email:{admin_val}"
            elif admin_val.startswith('ou_'):
                owner_arg = f"openid:{admin_val}"
            else:
                owner_arg = f"userid:{admin_val}"
            
    if owner_arg:
        try:
            member_type, member_id = owner_arg.split(':', 1)
            print(f"⚙️ 正在转移文档所有权至: {member_id} ({member_type})...")
            feishu_api.transfer_document_owner(token, document_id, member_type.strip(), member_id.strip())
            print(f"✅ 所有权转移成功")
        except ValueError:
            print("⚠️ 转移失败: owner 参数格式必须为 type:id，例如 email:you@example.com")
        except Exception as e:
            print(f"⚠️ 转移失败: {e}")
            
    print("📝 开始插入内容...")
    
    insert_index = 0
    success_count = 0
    fail_count = 0
    simple_batch = []
    
    def flush_simple_batch():
        nonlocal insert_index, success_count, fail_count, simple_batch
        if not simple_batch: return
        batch_blocks = [clean_block_for_children(b) for b in simple_batch]
        try:
            feishu_api.insert_children(token, document_id, document_id, batch_blocks, insert_index)
            insert_index += len(batch_blocks)
            success_count += len(batch_blocks)
        except Exception:
            for block in batch_blocks:
                try:
                    feishu_api.insert_children(token, document_id, document_id, [block], insert_index)
                    insert_index += 1
                    success_count += 1
                except Exception:
                    fail_count += 1
                time.sleep(0.1)
        simple_batch = []
        time.sleep(0.2)
        
    for block_id in first_level_block_ids:
        block = block_map.get(block_id)
        if not block: continue
        
        if block['block_type'] == 31:
            flush_simple_batch()
            try:
                res = rebuild_table_for_descendant(block, block_map)
                feishu_api.insert_descendant(token, document_id, document_id, res['children_id'], res['descendants'], insert_index)
                insert_index += 1
                success_count += 1
            except Exception as e:
                fail_count += 1
                try:
                    fb = table_to_text_blocks(block, block_map)
                    feishu_api.insert_children(token, document_id, document_id, fb, insert_index)
                    insert_index += len(fb)
                except Exception:
                    pass
            time.sleep(0.3)
            
        elif block['block_type'] == 27:
            flush_simple_batch()
            try:
                resp_data = feishu_api.insert_children(token, document_id, document_id, [clean_block_for_children(block)], insert_index)
                insert_index += 1
                success_count += 1
                
                children = resp_data.get('data', {}).get('children', [])
                if children:
                    new_block_id = children[0]['block_id']
                    img_url = image_url_map.get(block_id)
                    if img_url:
                        img_path = os.path.join(os.path.dirname(file_path), img_url)
                        if local_file.file_exists(img_path):
                            print(f"📸 上传图片: {img_path}")
                            file_info = local_file.read_binary_file_info(img_path)
                            file_token = feishu_api.upload_image_data(token, new_block_id, file_info)
                            feishu_api.update_block_image(token, document_id, new_block_id, file_token)
                        else:
                            print(f"⚠️ 图片文件不存在，无法上传: {img_path}")
            except Exception as e:
                print(f"❌ 处理图片块失败: {e}")
                fail_count += 1
            time.sleep(0.3)
            
        else:
            simple_batch.append(block)
            
    flush_simple_batch()
    
    print("\n✅ 文档发布完成")
    print(f"📄 文档标题: {title}")
    print(f"📄 文档 ID: {document_id}")
    print(f"🔗 文档链接: https://feishu.cn/docx/{document_id}")
    print(f"📊 成功: {success_count}, 失败: {fail_count}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"❌ 发布失败: {e}")
        sys.exit(1)
