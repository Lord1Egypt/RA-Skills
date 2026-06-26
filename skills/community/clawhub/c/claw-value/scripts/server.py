#!/usr/bin/env python3
"""
ClawValue 后端服务

提供 RESTful API 和静态文件服务。

API 端点:
- GET /api/         - 仪表盘主数据
- GET /api/stats    - 统计数据
- GET /api/skills   - 技能列表
- GET /api/sessions - 会话历史
- GET /api/evaluation - 评估结果
- POST /api/refresh - 刷新数据
- GET /api/health   - 健康检查

参考文档: docs/OPENCLAW_REFERENCE.md
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from flask import Flask, jsonify, send_from_directory, request
from functools import wraps
import time

# 添加 lib 目录到路径
lib_path = os.path.join(os.path.dirname(__file__), '..', 'lib')
sys.path.insert(0, lib_path)

# 导入核心模块
from collector import DataCollector
from evaluation import EvaluationEngine
from constants import DepthLevel, LobsterLevel, Achievement
from models import ClawValueDB

# 全局数据库实例
_db_instance = None

# 简单的内存缓存
_cache = {}
_CACHE_TTL = 60  # 缓存有效期（秒）

def get_cache(key):
    """获取缓存"""
    if key in _cache:
        data, timestamp = _cache[key]
        if time.time() - timestamp < _CACHE_TTL:
            return data
        else:
            del _cache[key]
    return None

def set_cache(key, data):
    """设置缓存"""
    _cache[key] = (data, time.time())

def clear_cache():
    """清空缓存"""
    global _cache
    _cache = {}

def cached(timeout=_CACHE_TTL):
    """缓存装饰器"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = f.__name__
            cached_data = get_cache(cache_key)
            if cached_data is not None:
                return jsonify(cached_data)
            result = f(*args, **kwargs)
            # 只缓存成功的响应
            if isinstance(result, tuple):
                data, status = result
                if status == 200:
                    set_cache(cache_key, data.get_json() if hasattr(data, 'get_json') else data)
            else:
                try:
                    set_cache(cache_key, result.get_json() if hasattr(result, 'get_json') else result)
                except:
                    pass
            return result
        return decorated_function
    return decorator

def get_db():
    """获取数据库实例（单例模式）"""
    global _db_instance
    if _db_instance is None:
        _db_instance = ClawValueDB()
    return _db_instance

# 创建 Flask 应用
web_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'web'))
app = Flask(__name__, static_folder=web_dir)

@app.route('/')
def index():
    """首页"""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/images/<path:filename>')
def serve_image(filename):
    """提供图片文件"""
    return send_from_directory(os.path.join(app.static_folder, 'images'), filename)


@app.route('/html2canvas.min.js')
def serve_html2canvas():
    """提供 html2canvas.min.js"""
    return send_from_directory(app.static_folder, 'html2canvas.min.js')


@app.route('/api/stats', methods=['GET'])
@cached()
def get_stats():
    """
    获取统计数据

    Returns:
        - skill_count: 技能总数
        - custom_skill_count: 自定义技能数
        - session_count: 会话总数
        - total_tokens: Token 消耗总量
        - usage_days: 使用天数
    """
    try:
        database = get_db()
        stats = database.get_latest_stats()
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/skills', methods=['GET'])
@cached()
def get_skills():
    """
    获取技能列表

    Query params:
        - category: 按类别筛选
        - custom_only: 仅显示自定义技能

    Returns:
        - skills: 技能列表
    """
    try:
        database = get_db()
        skills = database.get_skill_list()

        # 可选筛选
        category = request.args.get('category')
        custom_only = request.args.get('custom_only', 'false').lower() == 'true'

        if category:
            skills = [s for s in skills if s.get('category') == category]
        if custom_only:
            skills = [s for s in skills if s.get('is_custom')]

        return jsonify({
            'success': True,
            'data': {
                'skills': skills,
                'total': len(skills)
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/sessions', methods=['GET'])
@cached()
def get_sessions():
    """
    获取会话历史

    Query params:
        - limit: 返回数量限制
        - offset: 偏移量

    Returns:
        - sessions: 会话列表
    """
    try:
        database = get_db()
        cursor = database.conn.cursor()

        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)

        cursor.execute('''
            SELECT * FROM sessions
            ORDER BY last_active DESC
            LIMIT ? OFFSET ?
        ''', (limit, offset))

        sessions = [dict(row) for row in cursor.fetchall()]

        # 获取总数
        cursor.execute('SELECT COUNT(*) FROM sessions')
        total = cursor.fetchone()[0]

        return jsonify({
            'success': True,
            'data': {
                'sessions': sessions,
                'total': total,
                'limit': limit,
                'offset': offset
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/evaluation', methods=['GET'])
def get_evaluation():
    """
    获取评估结果

    Query params:
        - refresh: 是否刷新数据

    Returns:
        - evaluation: 评估结果
    """
    try:
        database = get_db()

        # 检查是否需要刷新
        refresh = request.args.get('refresh', 'false').lower() == 'true'

        if refresh:
            # 重新采集数据
            collector = DataCollector()
            data = collector.collect()
            data_dict = data.to_dict()

            # 评估
            engine = EvaluationEngine()
            evaluation = engine.generate_full_evaluation(data_dict)

            # 存储到数据库
            database.insert_collection_record({
                'total_sessions': data_dict.get('total_sessions', 0),
                'total_skills': data.total_skills,
                'total_agents': data_dict.get('config', {}).get('agent_count', 1) if data_dict.get('config') else 1,
                'total_tokens': data_dict.get('total_tokens', 0),
                'usage_days': data.usage_days,
                'error_count': data.log_stats.error_count
            })

            for skill in data_dict.get('skills', []):
                database.insert_skill(skill)

            database.insert_evaluation({
                'usage_level': evaluation.get('usage_level', 1),
                'value_estimate': evaluation.get('value_estimate', '0元'),
                'lobster_skill': evaluation.get('lobster_skill', ''),
                'skill_score': evaluation.get('skill_score', 0),
                'automation_score': evaluation.get('automation_score', 0),
                'integration_score': evaluation.get('integration_score', 0),
                'total_score': evaluation.get('total_score', 0),
                'raw_data': json.dumps(evaluation.get('raw_data', {}), ensure_ascii=False)
            })

            return jsonify({
                'success': True,
                'data': evaluation,
                'refreshed': True
            })
        else:
            # 返回最近的评估结果
            history = database.get_evaluation_history(limit=1)
            if history:
                evaluation = history[0]
                # 解析 raw_data
                if evaluation.get('raw_data'):
                    try:
                        evaluation['raw_data'] = json.loads(evaluation['raw_data'])
                    except:
                        pass
                return jsonify({
                    'success': True,
                    'data': evaluation,
                    'refreshed': False
                })
            else:
                # 没有历史数据，触发首次采集
                return get_evaluation_internal()
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def get_evaluation_internal():
    """内部评估方法"""
    collector = DataCollector()
    data = collector.collect()
    data_dict = data.to_dict()

    engine = EvaluationEngine()
    evaluation = engine.generate_full_evaluation(data_dict)

    database = get_db()
    database.insert_collection_record({
        'total_sessions': data_dict.get('total_sessions', 0),
        'total_skills': data.total_skills,
        'total_agents': data_dict.get('config', {}).get('agent_count', 1) if data_dict.get('config') else 1,
        'total_tokens': data_dict.get('total_tokens', 0),
        'usage_days': data.usage_days,
        'error_count': data.log_stats.error_count
    })

    for skill in data_dict.get('skills', []):
        database.insert_skill(skill)

    database.insert_evaluation({
        'usage_level': evaluation.get('usage_level', 1),
        'value_estimate': evaluation.get('value_estimate', '0元'),
        'lobster_skill': evaluation.get('lobster_skill', ''),
        'skill_score': evaluation.get('skill_score', 0),
        'automation_score': evaluation.get('automation_score', 0),
        'integration_score': evaluation.get('integration_score', 0),
        'total_score': evaluation.get('total_score', 0),
        'raw_data': json.dumps(evaluation.get('raw_data', {}), ensure_ascii=False)
    })

    return jsonify({
        'success': True,
        'data': evaluation,
        'refreshed': True
    })


@app.route('/api/refresh', methods=['POST'])
def refresh_data():
    """
    刷新数据

    手动触发数据重新采集
    """
    try:
        # 清除缓存
        clear_cache()
        
        collector = DataCollector()
        data = collector.collect()
        data_dict = data.to_dict()

        engine = EvaluationEngine()
        evaluation = engine.generate_full_evaluation(data_dict)

        database = get_db()

        # 插入采集记录
        database.insert_collection_record({
            'total_sessions': data_dict.get('total_sessions', 0),
            'total_skills': data.total_skills,
            'total_agents': data_dict.get('config', {}).get('agent_count', 1) if data_dict.get('config') else 1,
            'total_tokens': data_dict.get('total_tokens', 0),
            'usage_days': data.usage_days,
            'error_count': data.log_stats.error_count
        })

        # 插入技能
        for skill in data_dict.get('skills', []):
            database.insert_skill(skill)

        # 插入评估结果
        database.insert_evaluation({
            'usage_level': evaluation.get('usage_level', 1),
            'value_estimate': evaluation.get('value_estimate', '0元'),
            'lobster_skill': evaluation.get('lobster_skill', ''),
            'skill_score': evaluation.get('skill_score', 0),
            'automation_score': evaluation.get('automation_score', 0),
            'integration_score': evaluation.get('integration_score', 0),
            'total_score': evaluation.get('total_score', 0),
            'raw_data': json.dumps(evaluation.get('raw_data', {}), ensure_ascii=False)
        })

        return jsonify({
            'success': True,
            'message': '数据已刷新',
            'data': evaluation
        })
    except Exception as e:
        import traceback
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/history', methods=['GET'])
def get_history():
    """
    获取历史评估记录

    Query params:
        - limit: 返回数量限制

    Returns:
        - history: 历史记录列表
    """
    try:
        database = get_db()
        limit = request.args.get('limit', 10, type=int)
        history = database.get_evaluation_history(limit=limit)

        # 解析 raw_data
        for record in history:
            if record.get('raw_data'):
                try:
                    record['raw_data'] = json.loads(record['raw_data'])
                except:
                    pass

        return jsonify({
            'success': True,
            'data': {
                'history': history,
                'total': len(history)
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/compare', methods=['GET'])
def compare_history():
    """
    历史对比接口

    比较当前数据与历史数据的变化

    Query params:
        - days: 对比天数（默认7天）

    Returns:
        - current: 当前数据
        - previous: 历史数据
        - changes: 变化详情
    """
    try:
        days = request.args.get('days', 7, type=int)
        database = get_db()

        # 获取当前评估
        current_list = database.get_evaluation_history(limit=1)
        current = current_list[0] if current_list else {}

        # 获取历史评估
        history = database.get_evaluation_history(limit=days + 1)
        previous = history[-1] if len(history) > 1 else {}

        # 计算变化
        changes = {}
        if current and previous:
            current_score = current.get('total_score', 0)
            previous_score = previous.get('total_score', 0)
            changes['total_score'] = {
                'current': current_score,
                'previous': previous_score,
                'change': current_score - previous_score,
                'percent': round((current_score - previous_score) / max(previous_score, 1) * 100, 1)
            }

            # 解析 raw_data 获取更多指标
            try:
                current_raw = json.loads(current.get('raw_data', '{}')) if current.get('raw_data') else {}
                previous_raw = json.loads(previous.get('raw_data', '{}')) if previous.get('raw_data') else {}

                changes['skill_count'] = {
                    'current': current_raw.get('total_skills', 0),
                    'previous': previous_raw.get('total_skills', 0),
                    'change': current_raw.get('total_skills', 0) - previous_raw.get('total_skills', 0)
                }

                changes['custom_skills'] = {
                    'current': current_raw.get('custom_skills', 0),
                    'previous': previous_raw.get('custom_skills', 0),
                    'change': current_raw.get('custom_skills', 0) - previous_raw.get('custom_skills', 0)
                }
            except:
                pass

        return jsonify({
            'success': True,
            'data': {
                'current': current,
                'previous': previous,
                'changes': changes,
                'days': days
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/export', methods=['GET'])
def export_all_data():
    """
    导出所有数据

    返回完整的评估数据，供用户保存或分享
    """
    try:
        collector = DataCollector()
        data = collector.collect()
        data_dict = data.to_dict()

        engine = EvaluationEngine()
        evaluation = engine.generate_full_evaluation(data_dict)

        export_data = {
            'exported_at': datetime.now().isoformat(),
            'version': '1.0',
            'evaluation': evaluation,
            'summary': {
                'depth_level': evaluation.get('usage_level', '未知'),
                'total_score': evaluation.get('total_score', 0),
                'skill_count': data.total_skills,
                'custom_skills': data.custom_skills,
                'achievements_count': len(evaluation.get('achievements', []))
            }
        }

        return jsonify({
            'success': True,
            'data': export_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
@cached(30)  # 健康检查缓存30秒
def health_check():
    """健康检查"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/generate-image', methods=['POST'])
def generate_image():
    """
    生成龙虾主题图片

    使用阿里云万象 API 生成个性化图片，保存到本地。

    Request Body:
        - level: 用户等级 (1-5)
        - style: 风格名称 (可选): cyberpunk, minimalist, cartoon, realistic, fantasy
        - achievements: 成就列表 (可选)

    Returns:
        - success: 是否成功
        - image_url: 本地图片路径
        - style: 使用的风格
        - prompt: 使用的提示词
    """
    try:
        # 导入图片生成模块
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
        from image_generator import WanxImageGenerator, LobsterPromptTemplates
        import requests as http_requests

        # 解析请求
        data = request.get_json() or {}
        level = data.get('level', 1)
        style = data.get('style')
        achievements = data.get('achievements', [])

        # 生成图片
        generator = WanxImageGenerator()
        result = generator.generate_lobster(
            level=level,
            style=style,
            achievements=achievements
        )

        if result.success:
            # 下载图片并保存到本地
            response = http_requests.get(result.image_url, timeout=30)
            if response.status_code == 200:
                # 生成文件名
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'lobster_{level}_{timestamp}.png'
                save_path = os.path.join(app.static_folder, 'images', 'generated', filename)
                
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                
                # 返回本地路径
                local_url = f'/images/generated/{filename}'
                return jsonify({
                    'success': True,
                    'data': {
                        'image_url': local_url,
                        'style': result.style,
                        'prompt': result.prompt,
                        'request_id': result.request_id
                    }
                })
            else:
                return jsonify({
                    'success': False,
                    'error': f'下载图片失败: {response.status_code}'
                }), 500
        else:
            return jsonify({
                'success': False,
                'error': result.error
            }), 500

    except Exception as e:
        import traceback
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/image-styles', methods=['GET'])
def get_image_styles():
    """
    获取可用的图片风格列表
    
    Returns:
        - styles: 风格列表
    """
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
        from image_generator import LobsterPromptTemplates
        
        styles = []
        for key, info in LobsterPromptTemplates.STYLES.items():
            styles.append({
                'id': key,
                'name': info['name']
            })
        
        return jsonify({
            'success': True,
            'data': {'styles': styles}
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/share-card', methods=['POST'])
def generate_share_card():
    """
    生成分享卡片数据
    
    返回用于生成分享海报的所有数据，包括：
    - 用户等级和评估结果
    - 趣味文案
    - 推荐的分享格式
    
    Returns:
        - share_card: 分享卡片数据
    """
    try:
        # 获取当前评估数据
        collector = DataCollector()
        data = collector.collect()
        data_dict = data.to_dict()
        
        engine = EvaluationEngine()
        evaluation = engine.generate_full_evaluation(data_dict)
        
        # 计算等级
        total_score = evaluation.get('total_score', 0)
        level = 1
        for lvl, threshold in sorted(DepthLevel.SCORE_THRESHOLDS.items()):
            if total_score >= threshold:
                level = lvl
        
        # 等级信息
        level_names = {
            1: ('🐣', '入门小白', '刚刚接触 OpenClaw'),
            2: ('🎮', '初级玩家', '开始使用基本功能'),
            3: ('💻', '中级开发者', '熟练使用各种技能'),
            4: ('🚀', '高级工程师', '自定义技能，深度集成'),
            5: ('🦞', '龙虾大师', '达到专家级别')
        }
        
        emoji, name, desc = level_names.get(level, level_names[1])
        
        # 趣味文案
        fun_messages = [
            f"我用 OpenClaw 省了 ¥{(data.log_stats.tool_calls * 10):,}！",
            f"我是 {name}，你是什么等级？",
            f"🦞 龙虾能力 Lv.{level}，来挑战我吧！",
            f"解锁了 {len(evaluation.get('achievements', []))} 个成就，你呢？"
        ]
        
        # 生成分享卡片数据
        share_card = {
            'level': level,
            'level_emoji': emoji,
            'level_name': name,
            'level_desc': desc,
            'total_score': total_score,
            'skill_count': data.total_skills,
            'custom_skills': data.custom_skills,
            'achievements': evaluation.get('achievements', [])[:3],  # 最多展示3个
            'value_estimate': evaluation.get('value_estimate', '0元'),
            # 新增：排名信息
            'rank_percentile': evaluation.get('rank_percentile', 10),
            'rank_title': evaluation.get('rank_title', '🐣 萌新入门'),
            'rare_titles': evaluation.get('rare_titles', [])[:3],  # 最多展示3个稀有称号
            'fun_messages': fun_messages,
            'share_text': f"🦞 我的 OpenClaw 龙虾等级：{emoji} Lv.{level} {name}\n\n{evaluation.get('rank_title', '')}\n💰 价值估算：{evaluation.get('value_estimate', '0元')}\n🛠️ 技能数量：{data.total_skills} 个\n🏆 成就：{len(evaluation.get('achievements', []))} 个已解锁\n\n来测测你的「龙虾能力」吧！",
            'generated_at': datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'data': share_card
        })
        
    except Exception as e:
        import traceback
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/', methods=['GET'])
@app.route('/api/dashboard', methods=['GET'])
@cached(30)  # 仪表盘数据缓存30秒
def get_dashboard():
    """
    获取仪表盘完整数据（前端主入口）

    Returns:
        - depth_level: 使用深度等级 (1-5)
        - depth_breakdown: 各维度得分
        - value_estimation: 价值估算
        - skills: 技能统计
        - sessions: 会话统计
        - trends: 使用趋势
    """
    try:
        # 使用新的数据采集模块
        collector = DataCollector()
        data = collector.collect()  # 返回 CollectionData 对象
        
        # 评估
        engine = EvaluationEngine()
        # 转换为字典格式供评估引擎使用
        data_dict = data.to_dict()
        evaluation = engine.generate_full_evaluation(data_dict)

        # 计算深度等级 (1-5)
        total_score = evaluation.get('total_score', 0)
        depth_level = 1
        for level, threshold in sorted(DepthLevel.SCORE_THRESHOLDS.items()):
            if total_score >= threshold:
                depth_level = level

        # 深度分布
        metrics = evaluation.get('metrics', {})
        depth_breakdown = [
            {'level': 1, 'name': '技能数量', 'count': metrics.get('skill_count', 0)},
            {'level': 2, 'name': '自定义技能', 'count': metrics.get('custom_skills', 0)},
            {'level': 3, 'name': '日志条目', 'count': data.log_stats.total_entries},
            {'level': 4, 'name': 'Agent数量', 'count': metrics.get('agent_count', 1)},
            {'level': 5, 'name': '集成渠道', 'count': metrics.get('channels', 0)}
        ]

        # 价值估算
        value_str = evaluation.get('value_estimate', '0元')
        try:
            value_amount = int(value_str.replace(',', '').replace('元', '').strip())
        except ValueError:
            value_amount = 0
            
        value_estimation = {
            'amount': value_amount,
            'description': evaluation.get('value_level', '基础价值级'),
            'hours_saved': data.log_stats.tool_calls,  # 用工具调用数估算
            'efficiency': min(int(total_score * 1.2), 200),
            'roi': f'{min(int(total_score / 10), 10)}x'
        }

        # 技能统计 - 使用新的数据模型
        skills = {
            'total': data.total_skills,
            'custom': data.custom_skills,
            'categories': data.categories
        }

        # 会话统计 - 使用新的数据模型
        sessions = {
            'total': data.log_stats.total_entries,
            'total_messages': data.log_stats.tool_calls,
            'avg_messages': data.log_stats.tool_calls // max(data.usage_days, 1),
            'active_days': data.usage_days
        }

        # 使用趋势（最近7天模拟）
        trends = []
        for i in range(6, -1, -1):
            date = datetime.now() - timedelta(days=i)
            trends.append({
                'date': date.strftime('%m-%d'),
                'count': max(0, data.log_stats.tool_calls // 7 + (7 - i) * 2)
            })

        # 成就列表
        achievements = evaluation.get('achievements', [])

        response_data = {
            'depth_level': depth_level,
            'depth_breakdown': depth_breakdown,
            'value_estimation': value_estimation,
            'skills': skills,
            'sessions': sessions,
            'trends': trends,
            'evaluation': evaluation,
            'achievements': achievements,
            'log_stats': {
                'total_entries': data.log_stats.total_entries,
                'info_count': data.log_stats.info_count,
                'warn_count': data.log_stats.warn_count,
                'error_count': data.log_stats.error_count,
                'tool_calls': data.log_stats.tool_calls,
                'model_calls': data.log_stats.model_calls
            }
        }

        return jsonify({
            'success': True,
            'data': response_data
        })
    except Exception as e:
        import traceback
        error_msg = str(e)
        traceback_str = traceback.format_exc()
        
        # 生产环境不应该暴露详细错误
        return jsonify({
            'success': False,
            'error': '服务器内部错误，请稍后重试',
            'error_detail': error_msg if os.environ.get('DEBUG') else None,
            'traceback': traceback_str if os.environ.get('DEBUG') else None
        }), 500


def main():
    """启动服务器"""
    import argparse
    parser = argparse.ArgumentParser(description='ClawValue 后端服务')
    parser.add_argument('--port', '-p', type=int, default=5002, help='服务端口')
    parser.add_argument('--host', '-H', default='127.0.0.1', help='绑定地址')
    parser.add_argument('--debug', '-d', action='store_true', help='调试模式')
    args = parser.parse_args()

    print(f"""
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║   🦞 ClawValue - OpenClaw Claw度评估系统                    ║
║                                                            ║
║   服务地址: http://{args.host}:{args.port}                    ║
║   API 文档: http://{args.host}:{args.port}/api/stats         ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
    """)

    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()