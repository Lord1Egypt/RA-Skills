#!/usr/bin/env python3
"""
ClawHub API 发布工具 - 发布飞书日历智能调度器技能包
"""

import os
import sys
import json
import hashlib
import requests
from datetime import datetime
import argparse

# API 配置
API_BASE = "https://clawhub.ai/api/v1"
TOKEN = "clh_SspeysnDJXJ0Zrwogveq8J07pC3cI1J_lY7_kT4DAZs"  # 用户提供的 token

def get_headers():
    """获取请求头"""
    return {
        "Authorization": f"Bearer {TOKEN}",
        "User-Agent": "FeishuCalendarScheduler/1.0.0"
    }

def test_token():
    """测试 API token 有效性"""
    url = f"{API_BASE}/whoami"
    headers = get_headers()
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        print("✅ API Token 验证成功")
        print(f"   用户: {data.get('user', {}).get('displayName', '未知')}")
        print(f"   Handle: {data.get('user', {}).get('handle', '未知')}")
        return True
        
    except Exception as e:
        print(f"❌ API Token 验证失败: {e}")
        if hasattr(e, 'response'):
            print(f"   状态码: {e.response.status_code}")
            print(f"   响应: {e.response.text[:200]}")
        return False

def get_file_info(zip_path):
    """获取文件信息"""
    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"文件不存在: {zip_path}")
    
    # 计算 SHA256
    sha256_hash = hashlib.sha256()
    with open(zip_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    
    file_size = os.path.getsize(zip_path)
    
    return {
        "path": os.path.basename(zip_path),
        "size": file_size,
        "sha256": sha256_hash.hexdigest(),
        "contentType": "application/zip"
    }

def upload_file(zip_path):
    """上传文件到 ClawHub 存储"""
    print(f"📤 上传文件: {os.path.basename(zip_path)}")
    
    url = f"{API_BASE}/storage/upload"  # 猜测的端点，可能需要调整
    headers = get_headers()
    
    try:
        with open(zip_path, "rb") as f:
            files = {"file": (os.path.basename(zip_path), f, "application/zip")}
            response = requests.post(url, headers=headers, files=files, timeout=30)
        
        response.raise_for_status()
        result = response.json()
        
        print(f"✅ 文件上传成功")
        print(f"   Storage ID: {result.get('storageId', '未知')}")
        return result.get("storageId")
        
    except Exception as e:
        print(f"⚠️  文件上传失败，尝试直接发布: {e}")
        return None

def get_skill_files(skill_dir):
    """获取技能目录中的所有文件"""
    allowed_extensions = {'.md', '.py', '.sh', '.json', '.txt', '.yaml', '.yml', '.js', '.ts', '.html', '.css'}
    exclude_dirs = {'.git', '__pycache__', '.idea', '.vscode', 'node_modules'}
    exclude_files = {'.DS_Store', 'Thumbs.db'}
    
    skill_files = []
    
    for root, dirs, files in os.walk(skill_dir):
        # 排除隐藏目录和不需要的目录
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('.')]
        
        for file in files:
            if file in exclude_files or file.startswith('.'):
                continue
            
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, skill_dir)
            
            # 检查文件扩展名
            _, ext = os.path.splitext(file)
            if ext.lower() in allowed_extensions or file in ['SKILL.md', 'README.md', 'install.sh', 'LICENSE']:
                skill_files.append((rel_path, file_path))
    
    return skill_files

def publish_skill_from_dir(skill_dir, max_retries=3):
    """
    从目录发布技能到 ClawHub
    
    参数:
    - skill_dir: 技能目录路径
    - max_retries: 最大重试次数
    """
    url = f"{API_BASE}/skills"
    headers = get_headers()
    
    # 技能元数据（使用ASCII字符）
    skill_data = {
        "slug": "feishu-calendar-scheduler",
        "displayName": "Feishu Calendar Intelligent Scheduler",
        "version": "1.0.0",
        "changelog": "Initial release: Intelligent time recommendation algorithm, batch meeting management, smart license system. Provides efficient schedule automation solutions for enterprises.",
        "tags": ["feishu", "calendar", "automation", "enterprise-tool", "ai-agent", "productivity", "scheduling", "meeting-management"],
        "forkOf": None
    }
    
    print("🔄 收集技能文件...")
    skill_files = get_skill_files(skill_dir)
    
    if not skill_files:
        print("❌ 未找到技能文件")
        return None
    
    print(f"📁 找到 {len(skill_files)} 个文件:")
    for rel_path, _ in skill_files[:10]:  # 只显示前10个
        print(f"   - {rel_path}")
    if len(skill_files) > 10:
        print(f"   ... 还有 {len(skill_files) - 10} 个文件")
    
    for attempt in range(max_retries):
        if attempt > 0:
            wait_time = 30 * attempt  # 递增等待时间
            print(f"⏳ 等待 {wait_time} 秒后重试 (尝试 {attempt + 1}/{max_retries})...")
            import time
            time.sleep(wait_time)
        
        print(f"🚀 尝试发布 (尝试 {attempt + 1}/{max_retries})...")
        
        # 准备文件上传数据
        files = []
        
        # 添加 payload
        files.append(("payload", (None, json.dumps(skill_data, ensure_ascii=False), "application/json")))
        
        # 添加所有技能文件
        for rel_path, file_path in skill_files:
            # 确定 MIME 类型
            _, ext = os.path.splitext(file_path)
            if ext == '.md':
                mime_type = 'text/markdown'
            elif ext == '.py':
                mime_type = 'text/x-python'
            elif ext == '.sh':
                mime_type = 'text/x-shellscript'
            elif ext == '.json':
                mime_type = 'application/json'
            elif ext == '.txt':
                mime_type = 'text/plain'
            else:
                mime_type = 'application/octet-stream'
            
            with open(file_path, 'rb') as f:
                file_content = f.read()
                # 检查是否是文本文件
                try:
                    file_content.decode('utf-8')
                    files.append(("files", (rel_path, file_content, mime_type)))
                except UnicodeDecodeError:
                    print(f"⚠️  跳过非文本文件: {rel_path}")
        
        if len(files) <= 1:  # 只有 payload
            print("❌ 没有有效的文本文件可上传")
            return None
        
        print(f"📤 上传 {len(files)-1} 个文件...")
        
        try:
            # 注意：requests 的 files 参数期望的是元组列表
            response = requests.post(url, headers=headers, files=files, timeout=60)
            response.raise_for_status()
            result = response.json()
            
            print("🎉 技能发布成功!")
            print(f"   Slug: {result.get('slug', '未知')}")
            print(f"   版本: {result.get('version', '未知')}")
            print(f"   创建时间: {result.get('createdAt', '未知')}")
            return result
            
        except requests.exceptions.HTTPError as e:
            error_msg = str(e)
            if "GitHub API rate limit" in error_msg or "rate limit" in error_msg.lower():
                print(f"⚠️  GitHub API 速率限制 (尝试 {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    continue
            
            print(f"❌ 发布失败: {e}")
            if hasattr(e, 'response'):
                print(f"   状态码: {e.response.status_code}")
                error_text = e.response.text[:500]
                print(f"   响应: {error_text}")
                
                # 尝试解析错误详情
                try:
                    error_json = e.response.json()
                    print(f"   错误详情: {json.dumps(error_json, ensure_ascii=False, indent=2)}")
                except:
                    pass
            return None
        except Exception as e:
            print(f"❌ 发布失败: {e}")
            return None
    
    print(f"❌ 经过 {max_retries} 次重试后仍失败")
    return None

def main():
    parser = argparse.ArgumentParser(description="ClawHub API 发布工具")
    parser.add_argument("--dir", default="..", 
                       help="技能目录路径")
    parser.add_argument("--test", action="store_true", help="仅测试 API token")
    parser.add_argument("--format", choices=["dir", "zip"], default="dir",
                       help="发布格式: dir=目录发布, zip=ZIP文件发布")
    
    args = parser.parse_args()
    
    # 解析目录路径
    skill_dir = args.dir
    if not os.path.isabs(skill_dir):
        skill_dir = os.path.join(os.path.dirname(__file__), skill_dir)
    
    print("🦞 ClawHub API 发布工具")
    print("=" * 50)
    
    # 测试 token
    if not test_token():
        print("❌ 无法继续，请检查 token")
        sys.exit(1)
    
    if args.test:
        print("✅ 测试完成")
        return
    
    # 检查目录
    if not os.path.isdir(skill_dir):
        print(f"❌ 技能目录不存在: {skill_dir}")
        sys.exit(1)
    
    print(f"📁 技能目录: {skill_dir}")
    print(f"📋 发布格式: {args.format}")
    print()
    
    # 发布技能
    if args.format == "dir":
        result = publish_skill_from_dir(skill_dir)
    else:
        # ZIP 格式（备用）
        zip_path = os.path.join(skill_dir, "feishu-calendar-scheduler.zip")
        if not os.path.exists(zip_path):
            print(f"❌ ZIP 文件不存在: {zip_path}")
            sys.exit(1)
        
        file_info = get_file_info(zip_path)
        print(f"📦 技能包信息:")
        print(f"   文件: {file_info['path']}")
        print(f"   大小: {file_info['size']:,} 字节")
        print(f"   SHA256: {file_info['sha256'][:16]}...")
        print()
        
        # 使用旧的 publish_skill 函数（如果保留的话）
        print("⚠️  ZIP格式发布可能不被支持（只允许文本文件）")
        result = None
    
    if result:
        print("\n✅ 发布完成!")
        print(f"📋 技能信息:")
        print(f"   名称: {result.get('displayName', '未知')}")
        print(f"   标识符: {result.get('slug', '未知')}")
        print(f"   版本: {result.get('version', '未知')}")
        print(f"   查看链接: https://clawhub.ai/skills/{result.get('slug', '')}")
        
        # 保存发布结果
        result_file = os.path.join(skill_dir, "publish_result.json")
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump({
                "published_at": datetime.now().isoformat(),
                "result": result
            }, f, indent=2, ensure_ascii=False)
        print(f"📝 发布结果已保存到: {result_file}")
    else:
        print("\n❌ 发布失败")
        sys.exit(1)

if __name__ == "__main__":
    main()