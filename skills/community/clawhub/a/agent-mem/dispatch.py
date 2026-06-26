#!/usr/bin/env python3
"""
调度中心 v2 - 统一版
用法:
  python3 dispatch.py check "任务"             → 检查是否需要调度
  python3 dispatch.py check --auto "任务"        → 检查并自动派发
  python3 dispatch.py report <agent> <结果>   → 记录结果
  python3 dispatch.py status                  → 查看状态
"""

import json, sys
from pathlib import Path
from datetime import datetime

INTENTS = {
    '数据分析': {
        'kw': ['数据','分析','报表','日报','异常','波动','转化率','GPM','gpm','复盘','看板'],
        'agents': ['data-assistant']
    },
    '内容创作': {
        'kw': ['文案','脚本','小红书','创作','内容','营销','推广','笔记','社媒'],
        'agents': ['xiaohongshu-agent', 'marketing-assistant']
    },
    '技术开发': {
        'kw': ['代码','开发','bug','报错','修复','API','脚本','Python','JS','编程','环境','代码问题'],
        'agents': ['tech-expert', 'code-architect']
    },
    '财务法务': {
        'kw': ['财务','发票','合同','法务','税务','报销','对账','合规','成本','毛利'],
        'agents': ['finance-assistant']
    },
    '新闻情报': {
        'kw': ['新闻','热点','行情','趋势','行业','竞品','最新消息'],
        'agents': ['news-assistant']
    },

    '金融投资': {
        'kw': ['股票','基金','投资','BTC','ETH','加密货币','行情分析','赚钱','亏钱','盈利','亏损','涨了','跌了','理财','收益','套利'],
        'agents': ['stock-analyst', 'finance-assistant']
    },
    '财务法务': {
        'kw': ['财务','发票','合同','法务','税务','报销','对账','合规','成本','毛利','赚钱','盈利','亏损','利润','支出','收入'],
        'agents': ['finance-assistant']
    },
    '广告投放': {
        'kw': ['广告','投放','千川','信息流','开户','审核','素材','消耗','ROI','roi','计划','计划组','创意','直播间'],
        'agents': ['advertising-agent', 'media-buyer']
    },
    '设计创意': {
        'kw': ['设计','海报','封面','主图','banner','图片','画图','logo','品牌','视觉'],
        'agents': ['designer']
    },
    '视频剪辑': {
        'kw': ['视频','剪辑','切片','混剪','录制','直播切片','视频处理','FFmpeg','转码'],
        'agents': ['video-editor']
    },
    '选品调研': {
        'kw': ['选品','竞品','热销','爆品','热销品','选品建议','市场调研','对标'],
        'agents': ['product-selector', 'intelligence-officer']
    },
    '短剧/漫剧': {
        'kw': ['短剧','漫剧','动态漫','热剧','短剧投放','短剧平台','短剧推广','短剧分销','微短剧','小程序短剧','IAA','ReelShort','DramaBox','付费短剧','短剧出海','短剧知识','短剧行业'],
        'agents': ['short-drama-expert']
    },
    'Agent管理': {
        'kw': ['Agent','agent','子Agent','子agent','注册','增删','删除Agent','创建Agent','添加Agent',
               '检查Agent','评估Agent','升级Agent','配置Agent','技能分配','状态监控',
               'Agent调度','Agent管理','团队管理','人事','优化Agent','Agent性能','Agent效率'],
        'agents': ['agent-admin']
    },
    '提示词优化': {
        'kw': ['提示词','prompt','agent人设','话术','角色设定','AI人设'],
        'agents': ['prompt-optimizer']
    },

    '职场助手': {
        'kw': ['职场','办公','周报','汇报','邮件','日程','排期','会议','纪要','请假','审批','文档','工作流','流程'],
        'agents': ['work-assistant']
    },
    '养鱼/水族': {
        'kw': ['养鱼','鱼缸','水族','观赏鱼','热带鱼','水质','过滤','水草','造景','灯鱼','孔雀鱼','金鱼','龙鱼','水族箱'],
        'agents': ['fish-hobbyist']
    },
    '考试备考': {
        'kw': ['考试','备考','复习','学习','刷题','题库','考试计划','知识梳理','重点'],
        'agents': ['exam-prep-assistant']
    },
    '系统维护': {
        'kw': ['运维','部署','重启','系统','服务','进程','日志','监控','备份','恢复','重启服务','部署服务','重装','环境配置'],
        'agents': ['tech-expert', 'tools-manager']
    },
}
class Dispatcher:
    def __init__(self, workspace):
        self.workspace = Path(workspace)
        self.data_file = self.workspace / '.dispatch-data.json'
        self.data = self._load()
    
    def _load(self):
        if self.data_file.exists():
            try: return json.load(open(self.data_file))
            except: pass
        return {'stats': {}, 'last': None, 'total': 0}
    
    def _save(self):
        json.dump(self.data, open(self.data_file, 'w'), indent=2, ensure_ascii=False)
    

    def _bm25_fallback(self, task):
        """兜底匹配（中文Jaccard不适用，保留接口供后续扩展）"""
        return None

    def _query_memory(self, task, intent):
        """从记忆系统查询历史任务（知识图谱+实体链接）"""
        try:
            import json
            results = {'memory_hits': 0, 'dispatch_history': []}
            
            # 查知识图谱
            kg_file = self.workspace / 'memory' / '.knowledge-graph.json'
            if kg_file.exists():
                kg = json.load(open(kg_file))
                nodes = kg.get('nodes', {})
                # 匹配所有dispatch记录
                for nid, n in nodes.items():
                    if n.get('type') == 'dispatch_record':
                        results['dispatch_history'].append({
                            'agent': n.get('agent',''),
                            'success_rate': n.get('success_rate',''),
                            'total': n.get('mention_count', 0)
                        })
            
            # 查实体链接
            link_file = self.workspace / 'memory' / '.entity-links.json'
            if link_file.exists():
                data = json.load(open(link_file))
                for e in data.get('entities', []):
                    if 'dispatch' in str(e.get('tags', [])):
                        results['memory_hits'] += 1
            
            return results if results['dispatch_history'] else None
        except:
            return None


    def _sr(self, agent):
        """Agent成功率"""
        s = self.data['stats'].get(agent, {})
        t = s.get('total', 0)
        return s.get('success', 0) / t if t > 0 else 0.5
    
    def check(self, task):
        tl = task.lower()
        best = None
        best_n = 0
        for name, rule in INTENTS.items():
            n = sum(1 for kw in rule['kw'] if kw.lower() in tl)
            if n > best_n:
                best_n = n
                best = name
        
        if best and best_n > 0:
            rule = INTENTS[best]
            agents = sorted(rule['agents'], key=lambda a: -self._sr(a))
            r = {
                'dispatch': True,
                'intent': best,
                'agent': agents[0],
                'agents': rule['agents'],
                'confidence': round(best_n / max(len(rule['kw']), 1) * 1.5, 2)
            }
        else:
            r = {'dispatch': False, 'intent': '通用', 'agent': 'main'}
        
        
        # 查询记忆系统：有没有类似任务的历史记录
        mem_info = self._query_memory(task, best if best else None)
        if mem_info:
            r['memory_hint'] = mem_info
        r['task'] = task
        r['ts'] = datetime.now().isoformat()
        self.data['last'] = r
        self._save()
        return r
    
    def report(self, agent, success, duration=None, notes='', reason=''):
        if not agent:
            last = self.data.get('last')
            if not last or 'agent' not in last:
                return {'error': '没有待报告的调度，请传agent名称'}
            agent = last['agent']
        
        if agent not in self.data['stats']:
            self.data['stats'][agent] = {'total': 0, 'success': 0, 'fail': 0, 'duration': 0, 'errors': []}
        
        s = self.data['stats'][agent]
        s['total'] += 1
        if success:
            s['success'] += 1
            if duration: s['duration'] += duration
        else:
            s['fail'] += 1
            if reason:
                s.setdefault('errors', []).append({
                    'reason': reason,
                    'time': datetime.now().isoformat(),
                    'notes': notes
                })
                # 只保留最近20条错误记录
                if len(s['errors']) > 20:
                    s['errors'] = s['errors'][-20:]
        
        self.data['total'] += 1
        self._save()
        
        # 🔥 同步到调度日志（HOT+COLD级）
        try:
            import sys
            from agent_mem.core import dispatch_logger
            
            last = self.data.get('last', {})
            dispatch_logger.log_dispatch(
                from_channel='webchat',  # 默认webchat，可改成传参
                from_agent='main',
                to_agent=agent,
                task=last.get('task', ''),
                intent=last.get('intent', ''),
                result='success' if success else 'fail',
                duration=duration or 0,
                detail=notes or reason
            )
        except Exception as e:
            pass  # 日志失败不影响主流程
        
        return {'ok': True, 'agent': agent, 'success': success}
    

    def auto_dispatch(self, result, gateway_url=''):
        """自动派发到目标Agent（需要自定义gateway_url）
        
        Args:
            result: dispatch.check() 的结果
            gateway_url: 消息网关URL（如 http://127.0.0.1:18789）
                         传空则不派发，只返回调度结果
        """
        agent = result.get('agent')
        task = result.get('task', '')
        intent = result.get('intent', '未知')
        
        if not agent or agent == 'main':
            return {'ok': False, 'reason': '无需派发'}
        
        if not gateway_url:
            return {'ok': True, 'agent': agent, 'dispatched': False,
                    'message': '未配置gateway_url，仅返回调度结果'}
        
        import requests
        try:
            payload = {
                'agentId': agent,
                'message': f"## {intent}任务\n\n{task}\n\n---\n*来源：调度系统自动派发*",
                'timeoutSeconds': 120
            }
            r = requests.post(
                f'{gateway_url.rstrip("/")}/api/sessions/send',
                json=payload,
                timeout=10
            )
            if r.status_code == 200:
                return {'ok': True, 'agent': agent, 'dispatched': True}
            return {'ok': False, 'error': f'HTTP {r.status_code}'}
        except Exception as e:
            return {'ok': False, 'error': str(e)}


    def status(self):
        done = sum(s.get('success', 0) for s in self.data['stats'].values())
        return {
            'total': self.data['total'],
            'rate': f"{done/max(self.data['total'],1)*100:.0f}%",
            'agents': self.data['stats']
        }

    def clear(self):
        """重置统计数据"""
        self.data = {'stats': {}, 'last': None, 'total': 0}
        self._save()
        return {'ok': True, 'msg': '已重置'}


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法: dispatch.py check/report/status/clear ...')
        sys.exit(1)
    
    d = Dispatcher(Path.home() / '.agent-mem')
    cmd = sys.argv[1]
    
    if cmd == 'check':
        if len(sys.argv) < 3:
            print(json.dumps({'error': '需要任务描述'}))
            sys.exit(1)
        result = d.check(' '.join(sys.argv[2:]))
        # 自动派发模式（加 --auto 参数）
        if '--auto' in sys.argv and result.get('dispatch'):
            dispatch_result = d.auto_dispatch(result)
            result['auto_dispatch'] = dispatch_result
        print(json.dumps(result, ensure_ascii=False))
    
    elif cmd == 'report':
        agent = sys.argv[2] if len(sys.argv) > 2 else ''
        result = sys.argv[3] if len(sys.argv) > 3 else 'success'
        success = result in ('success', 'ok', 'true')
        dur = None
        for a in sys.argv[4:]:
            if a.startswith('d='):
                try: dur = float(a[2:])
                except: pass
        print(json.dumps(d.report(agent, success, dur), ensure_ascii=False))
    
    elif cmd == 'status':
        print(json.dumps(d.status(), ensure_ascii=False, indent=2))
    
    elif cmd == 'clear':
        print(json.dumps(d.clear(), ensure_ascii=False))
    
    else:
        print(f'未知: {cmd}')
