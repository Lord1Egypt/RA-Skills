#!/usr/bin/env python3
"""
Echo Seed Web 端 - Flask 后端

提供 REST API 和 Web 界面
"""

from flask import Flask, render_template, jsonify, request, Response
import sqlite3
import json
import csv
import io
import requests
from datetime import datetime, timedelta
from pathlib import Path
import sys

# API 配置
NOTION_API_KEY = 'YOUR_MATON_API_KEY'
NOTION_BASE_URL = 'https://gateway.maton.ai/notion/v1/'
GOOGLE_CALENDAR_BASE_URL = 'https://gateway.maton.ai/google-calendar/calendar/v3/'

# Telegram 配置（用于发送 Notion 链接通知）
# 使用 OpenClaw 的 message 工具发送，而不是直接调用 Telegram API

# 获取项目根目录
ROOT_DIR = Path(__file__).parent.parent

# 初始化 Flask，明确指定模板和静态文件路径
app = Flask(__name__,
            template_folder=str(ROOT_DIR / 'templates'),
            static_folder=str(ROOT_DIR / 'static'))

# 导入数据库助手（带超时和重试）
from db_helper import get_db_connection, execute_query, init_db, DB_PATH

# 种子类型配置（颜色）
CAPSULE_CONFIG = {
    'note': {'name': '笔记', 'emoji': '📝', 'color': '#6B7280', 'bg': '#F3F4F6'},
    'idea': {'name': '灵感', 'emoji': '💡', 'color': '#F59E0B', 'bg': '#FEF3C7'},
    'link': {'name': '链接', 'emoji': '🔗', 'color': '#3B82F6', 'bg': '#DBEAFE'},
    'diary': {'name': '日记', 'emoji': '📔', 'color': '#10B981', 'bg': '#D1FAE5'},
    'thought': {'name': '思考', 'emoji': '💭', 'color': '#8B5CF6', 'bg': '#EDE9FE'},
    'collection': {'name': '收藏', 'emoji': '⭐', 'color': '#EC4899', 'bg': '#FCE7F3'},
    'todo': {'name': '待办', 'emoji': '✅', 'color': '#EF4444', 'bg': '#FEE2E2'},
    'voice': {'name': '语音', 'emoji': '🎤', 'color': '#06B6D4', 'bg': '#CFFAFE'},
}

# 状态配置
STATUS_CONFIG = {
    'active': {'name': '活跃', 'color': '#10B981'},
    'completed': {'name': '已完成', 'color': '#6B7280'},
    'archived': {'name': '已归档', 'color': '#9CA3AF'},
}


def get_db():
    """获取数据库连接（使用 db_helper）"""
    return get_db_connection()


# 闪电种子父页面 ID
NOTION_PARENT_PAGE_ID = 'YOUR_NOTION_PARENT_PAGE_ID'


def send_telegram_notion_link(title, notion_url, capsule_type):
    """发送 Notion 链接到 Telegram - 通过写入通知队列文件"""
    try:
        type_emoji = CAPSULE_CONFIG.get(capsule_type, {}).get('emoji', '📝')
        type_name = CAPSULE_CONFIG.get(capsule_type, {}).get('name', capsule_type)
        
        message = f"""✅ 种子已同步到 Notion

{type_emoji} {title or 'Untitled Seed'}
类型：{type_name}

🔗 查看：{notion_url}
""".strip()
        
        # 写入通知队列文件，由外部脚本发送到 Telegram
        queue_file = ROOT_DIR / 'logs' / 'notion_notification_queue.json'
        queue_file.parent.mkdir(parents=True, exist_ok=True)
        
        notification = {
            'timestamp': datetime.now().isoformat(),
            'type': 'notion_sync',
            'capsule_type': capsule_type,
            'title': title,
            'notion_url': notion_url,
            'message': message
        }
        
        with open(queue_file, 'w', encoding='utf-8') as f:
            json.dump(notification, f, ensure_ascii=False, indent=2)
        
        print(f"Notion 通知已写入队列：{queue_file}")
    except Exception as e:
        print(f"Telegram 通知错误：{e}")


def sync_to_notion(capsule_id, capsule_type, title, content, tags):
    """同步种子到 Notion - 所有种子作为子页面挂到闪电种子父页面下
    
    返回：(notion_page_id, notion_url) 或 (None, None)
    """
    try:
        headers = {
            'Authorization': f'Bearer {NOTION_API_KEY}',
            'Notion-Version': '2025-09-03',
            'Content-Type': 'application/json'
        }
        
        # 构建页面内容
        type_emoji = CAPSULE_CONFIG.get(capsule_type, {}).get('emoji', '📝')
        
        # 所有种子都作为闪电种子页面的子页面
        page_data = {
            'parent': {'type': 'page_id', 'page_id': NOTION_PARENT_PAGE_ID},
            'properties': {
                'title': [
                    {
                        'text': {
                            'content': f"{type_emoji} {title or 'Untitled Seed'}"
                        }
                    }
                ]
            },
            'children': [
                {
                    'object': 'block',
                    'type': 'paragraph',
                    'paragraph': {
                        'rich_text': [
                            {
                                'type': 'text',
                                'text': {
                                    'content': content or ''
                                }
                            }
                        ]
                    }
                }
            ]
        }
        
        if tags:
            page_data['children'].append({
                'object': 'block',
                'type': 'paragraph',
                'paragraph': {
                    'rich_text': [
                        {
                            'type': 'text',
                            'text': {
                                'content': f'Tags: {tags}'
                            }
                        }
                    ]
                }
            })
        
        response = requests.post(
            f'{NOTION_BASE_URL}pages',
            headers=headers,
            json=page_data,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            page_id = result.get('id')
            page_url = result.get('url')
            return page_id, page_url
        else:
            print(f"Notion sync failed: {response.status_code} - {response.text}")
            return None, None
            
    except Exception as e:
        print(f"Notion sync error: {e}")
        return None, None


def sync_to_calendar(capsule_id, title, content, reminder_at):
    """同步待办事项到 Google Calendar"""
    try:
        if not reminder_at:
            return None
        
        headers = {
            'Authorization': f'Bearer {NOTION_API_KEY}',  # 使用相同的 API key
            'Content-Type': 'application/json'
        }
        
        # 解析提醒时间
        try:
            reminder_dt = datetime.fromisoformat(reminder_at.replace('Z', '+00:00'))
        except:
            reminder_dt = datetime.now() + timedelta(days=1)
        
        event_data = {
            'summary': f'✅ {title or "Seed Reminder"}',
            'description': content or '',
            'start': {
                'dateTime': reminder_dt.isoformat(),
                'timeZone': 'Asia/Shanghai'
            },
            'end': {
                'dateTime': (reminder_dt + timedelta(hours=1)).isoformat(),
                'timeZone': 'Asia/Shanghai'
            }
        }
        
        response = requests.post(
            f'{GOOGLE_CALENDAR_BASE_URL}calendars/primary/events',
            headers=headers,
            json=event_data,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            return result.get('id')
        else:
            print(f"Calendar sync failed: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Calendar sync error: {e}")
        return None


@app.route('/')
def index():
    """Web 界面"""
    return render_template('index.html')


@app.route('/api/capsules', methods=['GET'])
def get_capsules():
    """获取种子列表"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # 获取查询参数
        capsule_type = request.args.get('type')
        status = request.args.get('status')
        search = request.args.get('search')
        limit = request.args.get('limit', 100)
        
        # 构建查询
        query = 'SELECT * FROM capsules WHERE 1=1'
        params = []
        
        if capsule_type:
            query += ' AND type = ?'
            params.append(capsule_type)
        
        if status:
            query += ' AND status = ?'
            params.append(status)
        
        if search:
            query += ' AND (title LIKE ? OR content LIKE ? OR tags LIKE ?)'
            search_param = f'%{search}%'
            params.extend([search_param, search_param, search_param])
        
        query += ' ORDER BY created_at DESC LIMIT ?'
        params.append(int(limit))
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        capsules = []
        for row in rows:
            capsule = dict(row)
            type_info = CAPSULE_CONFIG.get(capsule['type'], {})
            capsule['type_name'] = type_info.get('name', capsule['type'])
            capsule['type_emoji'] = type_info.get('emoji', '')
            capsule['type_color'] = type_info.get('color', '#6B7280')
            capsule['type_bg'] = type_info.get('bg', '#F3F4F6')
            capsules.append(capsule)
        
        return jsonify({'success': True, 'data': capsules, 'count': len(capsules)})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/capsules', methods=['POST'])
def create_capsule():
    """创建种子（自动 AI 分析）"""
    import sys
    sys.stderr.write("🔥🔥🔥 create_capsule CALLED! 🔥🔥🔥\n")
    sys.stderr.flush()
    
    try:
        data = request.json
        capsule_id = data.get('id', datetime.now().strftime('%Y%m%d%H%M%S%f'))
        created_at = datetime.now().isoformat()
        
        capsule_type = data.get('type', 'note')
        title = data.get('title', '')
        content = data.get('content', '')
        url = data.get('url', '')
        tags = data.get('tags', '')
        reminder_at = data.get('reminder_at')
        
        conn = get_db()
        cursor = conn.cursor()
        
        sys.stderr.write(f"1️⃣ 准备插入种子\n")
        sys.stderr.flush()
        
        # 先插入种子
        cursor.execute('''
            INSERT INTO capsules 
            (id, type, title, content, url, tags, created_at, reminder_at, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            capsule_id,
            capsule_type,
            title,
            content,
            url,
            tags,
            created_at,
            reminder_at,
            json.dumps(data.get('metadata', {}))
        ))
        conn.commit()  # 先提交，确保 AI 分析能读取
        
        sys.stderr.write(f"2️⃣ 种子已插入，开始 AI 分析\n")
        sys.stderr.flush()
        
        # ========== 自动 AI 分析 ==========
        auto_tags = []
        sys.stderr.write(f"🤖 AI 分析开始：type={capsule_type}, url={url}, len={len(content)}\n")
        sys.stderr.flush()
        
        # 1. 链接分析（如果有 URL）
        if url:
            print(f"  → 执行链接分析")
            try:
                from ai_service import analyze_link
                ai_result = analyze_link(capsule_id, url)
                if ai_result.get('success'):
                    auto_tags.extend(ai_result.get('suggested_tags', []))
                    print(f"  ✅ 链接分析成功，标签：{auto_tags}")
            except Exception as e:
                print(f"  ❌ AI 链接分析失败：{e}")
        
        # 2. 点子扩张（如果是 idea 类型或内容较短）
        elif capsule_type == 'idea' or (content and len(content) < 50):
            sys.stderr.write(f"  → 执行点子扩张 (type={capsule_type}, len={len(content)})\n")
            sys.stderr.flush()
            try:
                from ai_service import analyze_expansion
                sys.stderr.write(f"    调用 analyze_expansion...\n")
                sys.stderr.flush()
                ai_result = analyze_expansion(capsule_id, content)
                sys.stderr.write(f"    AI 结果：{ai_result.get('success')}\n")
                sys.stderr.flush()
                if ai_result.get('success'):
                    auto_tags.extend(ai_result.get('suggested_tags', []))
                    sys.stderr.write(f"  ✅ 点子扩张成功，标签：{auto_tags}\n")
                    sys.stderr.flush()
            except Exception as e:
                sys.stderr.write(f"  ❌ AI 点子扩张失败：{e}\n")
                sys.stderr.flush()
                import traceback
                traceback.print_exc()
        else:
            print(f"  ⚠️ 不满足 AI 分析条件：type={capsule_type}, url={url}, len={len(content)}")
        
        # 3. 智能关联（所有种子）
        print(f"  → 执行智能关联")
        try:
            from ai_service import find_relations
            relations = find_relations(capsule_id)
            if relations.get('success'):
                print(f"  ✅ 找到 {len(relations.get('relations', []))} 个相关种子")
        except Exception as e:
            print(f"  ❌ AI 智能关联失败：{e}")
        
        # 合并自动标签
        if auto_tags:
            final_tags = tags + ',' + ','.join(auto_tags[:5]) if tags else ','.join(auto_tags[:5])
            cursor.execute("UPDATE capsules SET tags = ? WHERE id = ?", (final_tags, capsule_id))
            conn.commit()  # 提交标签更新
            print(f"  ✅ AI 标签已更新：{final_tags}")
        else:
            print(f"  ⚠️ 无自动标签生成")
        # ==================================
        
        # 同步到 Notion
        notion_page_id, notion_url = sync_to_notion(capsule_id, capsule_type, title, content, tags)
        
        # 发送 Telegram 通知（如果 Notion 同步成功）- 直接通过 OpenClaw message 工具
        if notion_url:
            # 写入通知队列，由心跳任务发送
            send_telegram_notion_link(title, notion_url, capsule_type)
        
        # 同步到 Google Calendar（仅待办类型且有提醒时间）
        calendar_event_id = None
        if capsule_type == 'todo' and reminder_at:
            calendar_event_id = sync_to_calendar(capsule_id, title, content, reminder_at)
        
        # 更新同步 ID
        if notion_page_id or calendar_event_id:
            updates = []
            params = []
            if notion_page_id:
                updates.append('notion_page_id = ?')
                params.append(notion_page_id)
            if calendar_event_id:
                updates.append('calendar_event_id = ?')
                params.append(calendar_event_id)
            params.append(capsule_id)
            cursor.execute(f"UPDATE capsules SET {', '.join(updates)} WHERE id = ?", params)
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'id': capsule_id, 'notion_page_id': notion_page_id, 'notion_url': notion_url, 'calendar_event_id': calendar_event_id, 'ai_tags': auto_tags})
    
    except Exception as e:
        print(f"Create capsule error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/capsules/<capsule_id>', methods=['PUT'])
def update_capsule(capsule_id):
    """更新种子"""
    try:
        data = request.json
        conn = get_db()
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        for field in ['title', 'content', 'url', 'tags', 'status', 'reminder_at']:
            if field in data:
                updates.append(f'{field} = ?')
                params.append(data[field])
        
        if not updates:
            return jsonify({'success': False, 'error': 'No fields to update'})
        
        params.append(capsule_id)
        query = f"UPDATE capsules SET {', '.join(updates)} WHERE id = ?"
        
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/capsules/<capsule_id>', methods=['DELETE'])
def delete_capsule(capsule_id):
    """删除种子"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM capsules WHERE id = ?', (capsule_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """获取统计信息"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # 总数
        cursor.execute('SELECT COUNT(*) FROM capsules')
        total = cursor.fetchone()[0]
        
        # 按类型统计
        cursor.execute('SELECT type, COUNT(*) FROM capsules GROUP BY type')
        by_type = dict(cursor.fetchall())
        
        # 按状态统计
        cursor.execute('SELECT status, COUNT(*) FROM capsules GROUP BY status')
        by_status = dict(cursor.fetchall())
        
        # 待办事项
        cursor.execute("SELECT COUNT(*) FROM capsules WHERE type = 'todo' AND status = 'active'")
        active_todos = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'success': True,
            'data': {
                'total': total,
                'by_type': by_type,
                'by_status': by_status,
                'active_todos': active_todos
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/export/<format>', methods=['GET'])
def export_capsules(format):
    """导出种子数据"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # 获取查询参数
        capsule_type = request.args.get('type')
        search = request.args.get('search')
        
        # 构建查询
        query = 'SELECT * FROM capsules WHERE 1=1'
        params = []
        
        if capsule_type:
            query += ' AND type = ?'
            params.append(capsule_type)
        
        if search:
            query += ' AND (title LIKE ? OR content LIKE ? OR tags LIKE ?)'
            search_param = f'%{search}%'
            params.extend([search_param, search_param, search_param])
        
        query += ' ORDER BY created_at DESC'
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        capsules = [dict(row) for row in rows]
        
        if format == 'json':
            return Response(
                json.dumps(capsules, ensure_ascii=False, indent=2),
                mimetype='application/json',
                headers={'Content-Disposition': 'attachment; filename=capsules.json'}
            )
        
        elif format == 'csv':
            output = io.StringIO()
            if capsules:
                writer = csv.DictWriter(output, fieldnames=capsules[0].keys())
                writer.writeheader()
                writer.writerows(capsules)
            return Response(
                output.getvalue(),
                mimetype='text/csv',
                headers={'Content-Disposition': 'attachment; filename=capsules.csv'}
            )
        
        elif format == 'markdown':
            md = "# Echo Seed Seeds\n\n"
            for c in capsules:
                md += f"## {c['title'] or 'Untitled'}\n\n"
                md += f"**类型:** {c['type']}  \n"
                md += f"**创建时间:** {c['created_at']}  \n"
                if c['tags']:
                    md += f"**标签:** {c['tags']}  \n"
                md += f"\n{c['content'] or ''}\n\n"
                if c['url']:
                    md += f"🔗 {c['url']}\n\n"
                md += "---\n\n"
            return Response(
                md,
                mimetype='text/markdown',
                headers={'Content-Disposition': 'attachment; filename=capsules.md'}
            )
        
        else:
            return jsonify({'success': False, 'error': 'Unsupported format'}), 400
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/export/stats', methods=['GET'])
def export_stats():
    """导出统计信息"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM capsules')
        total = cursor.fetchone()[0]
        
        cursor.execute('SELECT type, COUNT(*) FROM capsules GROUP BY type')
        by_type = dict(cursor.fetchall())
        
        cursor.execute('SELECT status, COUNT(*) FROM capsules GROUP BY status')
        by_status = dict(cursor.fetchall())
        
        cursor.execute("SELECT COUNT(*) FROM capsules WHERE type = 'todo' AND status = 'active'")
        active_todos = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'success': True,
            'data': {
                'total': total,
                'by_type': by_type,
                'by_status': by_status,
                'active_todos': active_todos
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ========== AI 分析 API 端点 ==========

@app.route('/api/capsule/<capsule_id>/analyze/expand', methods=['POST'])
def api_analyze_expansion(capsule_id):
    """AI 点子扩张"""
    try:
        from ai_service import analyze_expansion, get_db
        
        # 获取种子内容
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT content FROM capsules WHERE id = ?', (capsule_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return jsonify({'code': 404, 'message': '种子不存在'}), 404
        
        content = row[0] or ''
        
        # 调用 AI 分析
        result = analyze_expansion(capsule_id, content)
        
        if result.get('success'):
            return jsonify({'code': 200, 'data': result})
        else:
            return jsonify({'code': 500, 'message': result.get('error', '分析失败')}), 500
    
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500


@app.route('/api/capsule/<capsule_id>/analyze/link', methods=['POST'])
def api_analyze_link(capsule_id):
    """AI 链接分析"""
    try:
        from ai_service import analyze_link, get_db
        
        # 获取种子 URL
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT url FROM capsules WHERE id = ?', (capsule_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row or not row[0]:
            return jsonify({'code': 400, 'message': '种子没有 URL'}), 400
        
        url = row[0]
        
        # 调用 AI 分析
        result = analyze_link(capsule_id, url)
        
        if result.get('success'):
            return jsonify({'code': 200, 'data': result})
        else:
            return jsonify({'code': 500, 'message': result.get('error', '分析失败')}), 500
    
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500


@app.route('/api/capsule/<capsule_id>/relations', methods=['GET'])
def api_get_relations(capsule_id):
    """获取关联种子"""
    try:
        from ai_service import find_relations
        
        result = find_relations(capsule_id)
        
        if result.get('success'):
            return jsonify({'code': 200, 'data': result})
        else:
            return jsonify({'code': 500, 'message': result.get('error', '查找失败')}), 500
    
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500


if __name__ == '__main__':
    # 确保数据库目录存在
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # 初始化数据库
    init_db()
    
    print("🚀 Echo Seed Web 端启动中...")
    print(f"📂 项目根目录：{ROOT_DIR}")
    print(f"📊 数据库路径：{DB_PATH}")
    print("📱 访问地址：http://localhost:5000")
    print("🌐 局域网访问：http://0.0.0.0:5000")
    print("🤖 AI 自动分析：已启用")
    
    # 关闭 debug 模式和 reloader 避免代码缓存
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
