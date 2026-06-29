#!/usr/bin/env python3
"""
昌叔专属软件开发助手 - v3.0.0
专注于系统、编程、数据库和AI开发的本地化智能助手

v3.0.0 改进:
- 版本号升级至 v3.0.0
- 修复 main() 中调用不存在的方法 (init/test_generate/test_run/test_analyze)
- review() 接入 code_scanner.py 做真实扫描，替代硬编码假数据
- diagnose() 接入 dameng_tool.py 做真实分析，替代硬编码假数据
- 删除 ai_enhanced_client.py 的 import 逻辑(污染主程序的假数据)
- LLMClient 和 SkillClient 保留(核心且可用)
- 配置热重载保留, bare except → except Exception
- 新子命令: sql(analyze/optimize/check/convert/format/connect),
             scan(security/quality), search(content/tags/semantic)
- 只导入存在的模块: dameng_tool, code_scanner, knowledge_searcher,
                     model_performance_monitor, prompt_template_manager
"""

import os
import sys
import argparse
import json
from pathlib import Path
from datetime import datetime
import requests
import time
import threading
import subprocess
import logging
import yaml

# 同目录模块导入
_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR))

from code_scanner import CodeScanner
from dameng_tool import DamengDatabaseTool
from knowledge_searcher import KnowledgeSearcher
from model_performance_monitor import ModelPerformanceMonitor
from prompt_template_manager import PromptTemplateManager


# =====================================================================
# LLMClient — 大模型客户端
# =====================================================================
class LLMClient:
    """大模型客户端 — 从config.yaml读取，无硬编码默认值"""

    # 不再硬编码模型名/API地址，全部从config或环境变量读取
    ENV_MAP = {
        'provider': 'LLM_PROVIDER',
        'api_key': 'LLM_API_KEY',
        'api_base': 'LLM_API_BASE',
        'model_name': 'LLM_MODEL_NAME',
    }

    def __init__(self, config):
        self.config = config.get('ai', {})
        # 优先环境变量 → config.yaml → 无默认值(必须显式配置)
        self.provider = self._resolve('provider')
        self.api_key = self._resolve('api_key')
        self.api_base = self._resolve('api_base')
        self.model_name = self._resolve('model_name')
        self.temperature = self.config.get('temperature', 0.7)
        self.max_tokens = self.config.get('max_tokens', 2000)
        self.timeout = self.config.get('timeout', 30)
        self.logger = logging.getLogger(__name__)

    def _resolve(self, key):
        """按优先级解析: 环境变量 → config.yaml，都不存在返回空字符串"""
        env_val = os.environ.get(self.ENV_MAP.get(key, ''), '')
        if env_val:
            return env_val
        return self.config.get(key, '')

    def is_configured(self):
        """检查是否配置了API密钥"""
        return bool(self.api_key)

    def call_llm(self, prompt, system_prompt=None):
        """调用大模型"""
        if not self.is_configured():
            return {
                "content": self._get_fallback_response(prompt),
                "model": "fallback",
                "tokens": {"prompt": 0, "completion": 0, "total": 0},
            }
        try:
            # provider 决定API调用格式: openai格式 | anthropic格式 | 自定义端点
            provider = (self.provider or '').lower()
            if provider == 'anthropic':
                return self._call_anthropic(prompt, system_prompt)
            elif provider == 'custom':
                return self._call_custom_api(prompt, system_prompt)
            else:
                # 默认走openai兼容格式(NVIDIA/DeepSeek/GLM等都兼容)
                return self._call_openai(prompt, system_prompt)
        except Exception as e:
            self.logger.error(f"调用大模型失败: {e}")
            return {
                "content": f"调用大模型失败: {e}\n\n{self._get_fallback_response(prompt)}",
                "model": "error",
                "tokens": {"prompt": 0, "completion": 0, "total": 0},
            }

    def _call_openai(self, prompt, system_prompt=None):
        """调用OpenAI兼容API (支持NVIDIA/DeepSeek等任何OpenAI格式端点)"""
        if not self.api_base:
            return {
                "content": "错误: 未配置api_base，请在config.yaml的ai段或环境变量LLM_API_BASE中设置",
                "model": "error",
                "tokens": {"prompt": 0, "completion": 0, "total": 0},
            }
        url = f"{self.api_base}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        data = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(url, headers=headers, json=data, timeout=self.timeout)
                response.raise_for_status()
                break
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    self.logger.warning(f"请求超时，正在进行第 {attempt + 1} 次重试")
                    time.sleep(2 ** attempt)
                else:
                    raise
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    self.logger.warning(f"请求失败，正在进行第 {attempt + 1} 次重试: {e}")
                    time.sleep(2 ** attempt)
                else:
                    raise
        result = response.json()
        usage = result.get('usage', {})
        tokens = {
            "prompt": usage.get('prompt_tokens', 0),
            "completion": usage.get('completion_tokens', 0),
            "total": usage.get('total_tokens', 0),
        }
        return {
            "content": result['choices'][0]['message']['content'],
            "model": result.get('model', self.model_name),
            "tokens": tokens,
        }

    def _call_anthropic(self, prompt, system_prompt=None):
        """调用Anthropic兼容API"""
        if not self.api_base:
            return {
                "content": "错误: 未配置api_base，请在config.yaml的ai段或环境变量LLM_API_BASE中设置",
                "model": "error",
                "tokens": {"prompt": 0, "completion": 0, "total": 0},
            }
        url = f"{self.api_base}/messages"
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        data = {
            "model": self.model_name,
            "max_tokens": self.max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system_prompt:
            data["system"] = system_prompt
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(url, headers=headers, json=data, timeout=self.timeout)
                response.raise_for_status()
                break
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    self.logger.warning(f"请求超时，正在进行第 {attempt + 1} 次重试")
                    time.sleep(2 ** attempt)
                else:
                    raise
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    self.logger.warning(f"请求失败，正在进行第 {attempt + 1} 次重试: {e}")
                    time.sleep(2 ** attempt)
                else:
                    raise
        result = response.json()
        usage = result.get('usage', {})
        tokens = {
            "prompt": usage.get('input_tokens', 0),
            "completion": usage.get('output_tokens', 0),
            "total": usage.get('input_tokens', 0) + usage.get('output_tokens', 0),
        }
        return {
            "content": result['content'][0]['text'],
            "model": result.get('model', self.model_name),
            "tokens": tokens,
        }

    def _call_custom_api(self, prompt, system_prompt=None):
        """调用自定义API"""
        if not self.api_base:
            return {
                "content": "错误: 自定义API需要配置api_base",
                "model": "error",
                "tokens": {"prompt": 0, "completion": 0, "total": 0},
            }
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        data = {
            "prompt": prompt,
            "model": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        if system_prompt:
            data["system_prompt"] = system_prompt
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(self.api_base, headers=headers, json=data, timeout=self.timeout)
                response.raise_for_status()
                break
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    self.logger.warning(f"请求超时，正在进行第 {attempt + 1} 次重试")
                    time.sleep(2 ** attempt)
                else:
                    raise
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    self.logger.warning(f"请求失败，正在进行第 {attempt + 1} 次重试: {e}")
                    time.sleep(2 ** attempt)
                else:
                    raise
        result = response.json()
        usage = result.get('usage', {})
        tokens = {
            "prompt": usage.get('prompt_tokens', usage.get('input_tokens', 0)),
            "completion": usage.get('completion_tokens', usage.get('output_tokens', 0)),
            "total": 0,
        }
        if tokens["total"] == 0:
            tokens["total"] = tokens["prompt"] + tokens["completion"]
        if isinstance(result, dict):
            content = result.get('response', result.get('text', result.get('content', str(result))))
        else:
            content = str(result)
        return {
            "content": content,
            "model": result.get('model', self.model_name) if isinstance(result, dict) else self.model_name,
            "tokens": tokens,
        }

    def _get_fallback_response(self, prompt):
        """获取备用响应（当没有配置API时）"""
        return f"""
问题: {prompt}

昌叔，关于这个问题，我建议：

1. **分析现状**
   - 评估当前的技术方案
   - 识别潜在的问题点
   - 考虑性能和可维护性

2. **提供方案**
   - 方案A: [具体方案]
   - 方案B: [具体方案]
   - 推荐方案: [推荐理由]

3. **实施建议**
   - 第一步: [具体步骤]
   - 第二步: [具体步骤]
   - 注意事项: [重要提醒]

需要我详细说明哪个部分吗？

---
提示: 要启用大模型功能，请在 config.yaml 中配置 api_key
"""


# =====================================================================
# SkillClient — 谨慎使用Hermes技能
# =====================================================================
class SkillClient:
    """Skill客户端 - 谨慎使用Hermes技能"""

    def __init__(self, config):
        self.config = config
        self.hermes_path = Path.home() / ".hermes"
        self.skills_path = self.hermes_path / "skills"

    def view_skill(self, skill_name):
        """查看skill详情"""
        try:
            for category_dir in self.skills_path.iterdir():
                if category_dir.is_dir():
                    skill_path = category_dir / skill_name
                    if skill_path.exists():
                        skill_file = skill_path / "SKILL.md"
                        if skill_file.exists():
                            with open(skill_file, 'r', encoding='utf-8') as f:
                                return f.read()
            result = subprocess.run(
                ["hermes", "skills", "inspect", skill_name],
                capture_output=True, text=True, timeout=10,
            )
            if result.returncode == 0:
                return result.stdout
            else:
                return f"查看skill失败: 本地和远程都找不到skill '{skill_name}'"
        except Exception as e:
            return f"查看skill失败: {e}"

    def call_skill(self, skill_name, args=None):
        """调用skill - 通过hermes chat预加载skill"""
        try:
            cmd = ["hermes", "chat", "-s", skill_name, "-Q"]
            if args:
                query = ' '.join(args)
                cmd.extend(["-q", query])
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                return result.stdout
            else:
                return f"调用skill失败: {result.stderr}"
        except subprocess.TimeoutExpired:
            return f"调用skill超时: {skill_name}"
        except Exception as e:
            return f"调用skill失败: {e}"


# =====================================================================
# ChangshuAssistant — 昌叔专属软件开发助手 v3.0.0
# =====================================================================
class ChangshuAssistant:
    """昌叔专属软件开发助手 v3.0.0"""

    def __init__(self, config_path=None):
        self.config_path = config_path
        if config_path is None:
            self.config_path = Path(__file__).resolve().parent.parent / "config.yaml"
        else:
            self.config_path = Path(config_path)

        self.config = self.load_config(self.config_path)
        self.name = "昌叔助手"
        self.version = "3.0.0"
        self.llm_client = LLMClient(self.config)
        self.skill_client = SkillClient(self.config)
        self.config_mtime = self._get_config_mtime()

        # 初始化子模块
        self.code_scanner = CodeScanner()
        self.dameng_tool = DamengDatabaseTool()
        self.knowledge_searcher = KnowledgeSearcher()
        self.model_monitor = ModelPerformanceMonitor()
        self.prompt_manager = PromptTemplateManager()
        self.logger = logging.getLogger(__name__)

        # 配置热重载监控线程
        self._config_watcher_running = True
        self._config_watcher_thread = threading.Thread(
            target=self._watch_config_changes, daemon=True,
        )
        self._config_watcher_thread.start()

    # -----------------------------------------------------------------
    # 配置管理
    # -----------------------------------------------------------------
    def _get_config_mtime(self):
        """获取配置文件修改时间"""
        try:
            return self.config_path.stat().st_mtime
        except Exception:
            return 0

    def _watch_config_changes(self):
        """监控配置文件变化（后台线程）"""
        while self._config_watcher_running:
            try:
                time.sleep(2)
                current_mtime = self._get_config_mtime()
                if current_mtime > self.config_mtime:
                    self.config_mtime = current_mtime
                    new_config = self.load_config(self.config_path)
                    self.config = new_config
                    self.llm_client = LLMClient(new_config)
                    print(f"\n[配置已自动更新] {datetime.now().strftime('%H:%M:%S')}")
            except Exception:
                pass

    def reload_config(self):
        """手动重新加载配置"""
        try:
            new_config = self.load_config(self.config_path)
            self.config = new_config
            self.llm_client = LLMClient(new_config)
            self.config_mtime = self._get_config_mtime()
            return f"配置已重新加载 - {datetime.now().strftime('%H:%M:%S')}"
        except Exception as e:
            return f"重新加载配置失败: {e}"

    def load_config(self, config_path=None):
        """加载配置文件"""
        if config_path is None:
            config_path = Path(__file__).resolve().parent.parent / "config.yaml"

        default_config = {
            "assistant": {
                "name": "昌叔助手",
                "personality": "专业、高效、贴心",
                "language": "zh-CN",
            },
            "features": {
                "system": True,
                "code": True,
                "database": True,
                "ai": True,
                "knowledge": True,
            },
            "integrations": {
                "claude_code": {
                    "enabled": True,
                    "path": "/usr/local/bin/claude",
                },
            },
            "preferences": {
                "output_format": "structured",
                "code_style": "pep8",
                "db_type": "dameng",
                "ai_provider": "local",
            },
        }

        if config_path.exists():
            try:
                import yaml
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = yaml.safe_load(f)
                    for key in user_config:
                        if key in default_config:
                            if isinstance(default_config[key], dict):
                                default_config[key].update(user_config[key])
                            else:
                                default_config[key] = user_config[key]
                        else:
                            default_config[key] = user_config[key]
            except ImportError:
                print("警告: 未安装pyyaml，使用默认配置")
            except Exception as e:
                print(f"警告: 加载配置文件失败: {e}")

        return default_config

    # -----------------------------------------------------------------
    # 问候 & 帮助 & 状态
    # -----------------------------------------------------------------
    def greet(self):
        """问候语"""
        return f"""
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║        {self.name} v{self.version}                          ║
║                                                            ║
║   专注于系统、编程、数据库和AI开发的本地化智能助手          ║
║                                                            ║
║   特性: 系统管理 | 代码开发 | 达梦数据库 | AI开发         ║
║   新增: SQL工具 | 代码扫描 | 知识搜索                     ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 准备就绪，昌叔！
"""

    def help(self):
        """显示帮助信息"""
        return """
使用方法:
  changshu-assistant <command> [subcommand] [options]

基础命令:
  chat              启动交互式对话
  ask <question>    直接提问
  review <path>     代码审查 (接入 code_scanner 真实扫描)
  diagnose          系统诊断 (接入 dameng_tool 真实分析)
  status            查看状态
  help              显示此帮助

SQL工具 (达梦数据库):
  sql analyze <file|sql>    分析SQL兼容性
  sql optimize <file|sql>   优化SQL语句
  sql check <file>          检查SQL文件达梦兼容性
  sql convert <file|sql>    SQL Server → 达梦语法转换
  sql format <file|sql>     格式化SQL
  sql connect               测试达梦数据库连接

代码扫描:
  scan security <path>      安全扫描
  scan quality <path>       代码质量分析

知识搜索:
  search content <query>    内容搜索
  search tags <tag1> [tag2] 标签搜索
  search semantic <query>    语义搜索

Skill调用:
  skill <name>               查看skill详情
  run <name>                 运行skill

示例:
  changshu-assistant chat
  changshu-assistant ask "如何优化达梦数据库查询？"
  changshu-assistant review app.py
  changshu-assistant sql analyze slow_query.sql
  changshu-assistant sql convert "SELECT TOP 10 * FROM t"
  changshu-assistant scan security ./src
  changshu-assistant search content "存储过程"
  changshu-assistant skill dameng-stored-procedure-review
"""

    def status(self):
        """显示状态信息"""
        features = []
        for feature, enabled in self.config['features'].items():
            status_mark = "✓" if enabled else "✗"
            features.append(f"  {status_mark} {feature}")

        integrations = []
        for integration, cfg in self.config['integrations'].items():
            status_mark = "✓" if cfg.get('enabled', False) else "✗"
            integrations.append(f"  {status_mark} {integration}")

        return f"""
{self.name} 状态信息
{'='*50}

版本: {self.version}
语言: {self.config['assistant']['language']}
性格: {self.config['assistant']['personality']}

功能模块:
{chr(10).join(features)}

集成服务:
{chr(10).join(integrations)}

用户偏好:
  输出格式: {self.config['preferences']['output_format']}
  代码风格: {self.config['preferences']['code_style']}
  数据库类型: {self.config['preferences']['db_type']}
  AI提供商: {self.config['preferences']['ai_provider']}

子模块:
  code_scanner:     ✓ 已加载
  dameng_tool:      ✓ 已加载
  knowledge_searcher: ✓ 已加载
  model_monitor:    ✓ 已加载
  prompt_manager:   ✓ 已加载
"""

    def view_skill(self, skill_name):
        """查看skill详情"""
        return self.skill_client.view_skill(skill_name)

    def run_skill(self, skill_name, args=None):
        """运行skill"""
        return self.skill_client.call_skill(skill_name, args)

    # -----------------------------------------------------------------
    # ask — 回答问题 (仅用 LLMClient)
    # -----------------------------------------------------------------
    def ask(self, question):
        """回答问题"""
        system_prompt = f"""你是{self.name}，一个专注于系统、编程、数据库和AI开发的本地化智能助手。

你的特点：
- 专业、高效、贴心
- 专注于达梦数据库、系统管理、代码开发
- 提供实用的技术建议和解决方案
- 回答简洁明了，重点突出

请用中文回答，提供具体、实用的建议。"""

        result = self.llm_client.call_llm(question, system_prompt)
        output = f"""{result['content']}

---
模型信息
  模型: {result['model']}
  Tokens: {result['tokens']['prompt']} (输入) + {result['tokens']['completion']} (输出) = {result['tokens']['total']} (总计)
"""
        return output

    # -----------------------------------------------------------------
    # review — 代码审查 (接入 code_scanner 真实扫描)
    # -----------------------------------------------------------------
    def review(self, file_path):
        """代码审查 — 接入 code_scanner.py 做真实扫描"""
        if not os.path.exists(file_path):
            return f"错误: 文件不存在 - {file_path}"

        # 安全扫描
        if os.path.isfile(file_path):
            vulnerabilities = self.code_scanner.scan_file(file_path)
            quality_results = [self.code_scanner.analyze_file(file_path)]
        else:
            vulnerabilities = self.code_scanner.scan_directory(file_path)
            quality_results = self.code_scanner.analyze_directory(file_path)

        # 重复代码检测
        duplicates = self.code_scanner.detect_duplicates(quality_results)

        # 生成报告
        report = self.code_scanner.generate_report(
            vulnerabilities=vulnerabilities,
            quality_results=quality_results,
            duplicates=duplicates,
        )
        return report

    # -----------------------------------------------------------------
    # diagnose — 系统诊断 (接入 dameng_tool 真实分析)
    # -----------------------------------------------------------------
    def diagnose(self):
        """系统诊断 — 接入 dameng_tool.py 做真实分析

        收集系统信息和达梦数据库兼容性分析能力
        """
        lines = []
        lines.append("=" * 50)
        lines.append("  系统诊断报告")
        lines.append("=" * 50)
        lines.append(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        # 1. 系统基本信息
        import platform
        lines.append(f"[系统]")
        lines.append(f"  平台: {platform.system()}")
        lines.append(f"  主机: {platform.node()}")
        lines.append(f"  Python: {platform.python_version()}")
        lines.append("")

        # 2. 达梦工具能力检测
        lines.append("[达梦数据库工具]")
        dm = self.dameng_tool
        pitfall_count = len(dm.COMMON_PITFALLS)
        type_count = len(dm.TYPE_MAPPINGS)
        lines.append(f"  已知达梦坑模式: {pitfall_count} 种")
        lines.append(f"  SQL Server→达梦 类型映射: {type_count} 种")
        lines.append(f"  dm_converter 可用: {'是' if dm._load_converter() else '否'}")
        lines.append("")

        # 3. 知识库检测
        lines.append("[知识库]")
        wiki_path = self.knowledge_searcher.wiki_path
        if os.path.isdir(wiki_path):
            md_count = 0
            for root, _dirs, files in os.walk(wiki_path):
                md_count += sum(1 for f in files if f.endswith('.md'))
            lines.append(f"  路径: {wiki_path}")
            lines.append(f"  Markdown文件数: {md_count}")
        else:
            lines.append(f"  路径: {wiki_path} (不存在)")
        lines.append("")

        # 4. 模型监控
        lines.append("[模型性能监控]")
        all_stats = self.model_monitor.get_all_stats()
        if all_stats:
            for model_name, stats in all_stats.items():
                lines.append(f"  {model_name}: 调用{stats['total_calls']}次, "
                             f"平均响应{stats['avg_response_time']:.2f}s")
        else:
            lines.append("  暂无性能数据")
        lines.append("")

        # 5. LLM 客户端状态
        lines.append("[LLM客户端]")
        lines.append(f"  已配置: {'是' if self.llm_client.is_configured() else '否'}")
        if self.llm_client.is_configured():
            lines.append(f"  提供商: {self.llm_client.provider}")
            lines.append(f"  模型: {self.llm_client.model_name}")
        lines.append("")

        lines.append("=" * 50)
        return "\n".join(lines)

    # -----------------------------------------------------------------
    # sql 子命令
    # -----------------------------------------------------------------
    def cmd_sql(self, subcmd, args):
        """SQL工具子命令分发"""
        subcmd = (subcmd or '').lower()

        if subcmd == 'analyze':
            target = args[0] if args else None
            if not target:
                return "错误: 请提供SQL文件路径或SQL语句"
            return self._sql_analyze(target)

        elif subcmd == 'optimize':
            target = args[0] if args else None
            if not target:
                return "错误: 请提供SQL文件路径或SQL语句"
            return self._sql_optimize(target)

        elif subcmd == 'check':
            target = args[0] if args else None
            if not target:
                return "错误: 请提供SQL文件路径"
            return self._sql_check(target)

        elif subcmd == 'convert':
            target = args[0] if args else None
            if not target:
                return "错误: 请提供SQL文件路径或SQL语句"
            return self._sql_convert(target)

        elif subcmd == 'format':
            target = args[0] if args else None
            if not target:
                return "错误: 请提供SQL文件路径或SQL语句"
            return self._sql_format(target)

        elif subcmd == 'connect':
            return self._sql_connect()

        else:
            return ("SQL子命令:\n"
                    "  analyze <file|sql>  - 分析SQL兼容性\n"
                    "  optimize <file|sql> - 优化SQL语句\n"
                    "  check <file>        - 检查SQL文件达梦兼容性\n"
                    "  convert <file|sql>  - SQL Server → 达梦转换\n"
                    "  format <file|sql>   - 格式化SQL\n"
                    "  connect             - 测试达梦数据库连接")

    def _read_sql_target(self, target):
        """读取SQL目标: 如果是文件路径则读文件内容，否则当作SQL语句"""
        if os.path.isfile(target):
            try:
                with open(target, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                return None, f"读取文件失败: {e}"
        return target, None

    def _sql_analyze(self, target):
        """分析SQL兼容性"""
        content, err = self._read_sql_target(target)
        if err:
            return err
        result = self.dameng_tool.analyze_sql(content)
        issues = result.get('issues', [])
        if not issues:
            return "SQL分析完成: 未发现达梦兼容性问题"

        lines = [f"SQL分析: {result.get('summary', '')}", "=" * 50]
        for issue in issues:
            severity = issue.get('severity', 'warning')
            lines.append(f"  [{severity.upper()}] {issue['description']}")
            lines.append(f"    次数: {issue.get('count', 1)}")
            lines.append(f"    建议: {issue.get('solution', '')}")
            lines.append(f"    示例: {issue.get('example', '')}")
            lines.append("")
        return "\n".join(lines)

    def _sql_optimize(self, target):
        """优化SQL语句"""
        content, err = self._read_sql_target(target)
        if err:
            return err
        optimized = self.dameng_tool.optimize_sql(content)
        return f"SQL优化结果:\n{'='*50}\n{optimized}"

    def _sql_check(self, target):
        """检查SQL文件的达梦兼容性"""
        if not os.path.isfile(target):
            return f"错误: 文件不存在 - {target}"
        result = self.dameng_tool.check_file(target)
        if 'error' in result:
            return f"检查失败: {result['error']}"

        issues = result.get('issues', [])
        lines = [f"文件兼容性检查: {target}",
                 f"行数: {result.get('line_count', 0)}",
                 f"{result.get('summary', '')}"]
        if not issues:
            lines.append("未发现兼容性问题")
        else:
            for issue in issues:
                lines.append(f"  [{issue.get('severity', 'warning').upper()}] {issue['description']}")
        return "\n".join(lines)

    def _sql_convert(self, target):
        """SQL Server → 达梦语法转换"""
        content, err = self._read_sql_target(target)
        if err:
            return err
        result = self.dameng_tool.convert_sqlserver_to_dm(content)
        if 'error' in result:
            lines = [f"转换失败: {result['error']}"]
            if 'fallback' in result:
                lines.append(f"\n降级优化结果:\n{result['fallback']}")
            return "\n".join(lines)

        lines = [f"转换完成, 变更数: {result.get('change_count', 0)}", "=" * 50]
        for change in result.get('changes', []):
            lines.append(f"  - {change}")
        lines.append(f"\n转换结果:\n{result.get('converted', '')}")
        return "\n".join(lines)

    def _sql_format(self, target):
        """格式化SQL"""
        content, err = self._read_sql_target(target)
        if err:
            return err
        formatted = self.dameng_tool.format_sql(content)
        return f"格式化结果:\n{'='*50}\n{formatted}"

    def _sql_connect(self):
        """测试达梦数据库连接"""
        result = self.dameng_tool.test_connect()
        if result.get('connected'):
            lines = ["连接成功!", "=" * 50]
            lines.append(f"  主机: {result.get('host', 'N/A')}:{result.get('port', 'N/A')}")
            if result.get('server_info'):
                lines.append(f"  版本: {result['server_info']}")
            if result.get('current_schema'):
                lines.append(f"  当前SCHEMA: {result['current_schema']}")
            if result.get('server_time'):
                lines.append(f"  服务器时间: {result['server_time']}")
            return "\n".join(lines)
        else:
            return f"连接失败: {result.get('error', '未知错误')}"

    # -----------------------------------------------------------------
    # scan 子命令
    # -----------------------------------------------------------------
    def cmd_scan(self, subcmd, args):
        """代码扫描子命令分发"""
        subcmd = (subcmd or '').lower()
        target = args[0] if args else '.'

        if subcmd == 'security':
            return self._scan_security(target)
        elif subcmd == 'quality':
            return self._scan_quality(target)
        else:
            return ("扫描子命令:\n"
                    "  security <path>  - 安全扫描\n"
                    "  quality <path>  - 代码质量分析")

    def _scan_security(self, target):
        """安全扫描"""
        if not os.path.exists(target):
            return f"错误: 路径不存在 - {target}"

        if os.path.isfile(target):
            vulnerabilities = self.code_scanner.scan_file(target)
        else:
            vulnerabilities = self.code_scanner.scan_directory(target)

        report = self.code_scanner.generate_report(vulnerabilities=vulnerabilities)
        return report

    def _scan_quality(self, target):
        """代码质量分析"""
        if not os.path.exists(target):
            return f"错误: 路径不存在 - {target}"

        if os.path.isfile(target):
            quality_results = [self.code_scanner.analyze_file(target)]
        else:
            quality_results = self.code_scanner.analyze_directory(target)

        duplicates = self.code_scanner.detect_duplicates(quality_results)
        report = self.code_scanner.generate_report(
            quality_results=quality_results, duplicates=duplicates,
        )
        return report

    # -----------------------------------------------------------------
    # search 子命令
    # -----------------------------------------------------------------
    def cmd_search(self, subcmd, args):
        """知识搜索子命令分发"""
        subcmd = (subcmd or '').lower()

        if subcmd == 'content':
            if not args:
                return "错误: 请提供搜索关键词"
            query = ' '.join(args)
            return self._search_content(query)
        elif subcmd == 'tags':
            if not args:
                return "错误: 请提供标签"
            return self._search_tags(args)
        elif subcmd == 'semantic':
            if not args:
                return "错误: 请提供搜索关键词"
            query = ' '.join(args)
            return self._search_semantic(query)
        else:
            return ("搜索子命令:\n"
                    "  content <query>       - 内容搜索\n"
                    "  tags <tag1> [tag2]... - 标签搜索\n"
                    "  semantic <query>      - 语义搜索")

    def _search_content(self, query):
        """内容搜索"""
        results = self.knowledge_searcher.search_content(query)
        if not results:
            return f"内容搜索 '{query}': 未找到结果"

        lines = [f"内容搜索 '{query}': 找到 {len(results)} 个文件", "=" * 50]
        for r in results:
            lines.append(f"  文件: {r['file']}")
            lines.append(f"  标题: {r.get('title', 'N/A')}")
            lines.append(f"  摘要: {r.get('snippet', '')[:120]}")
            lines.append(f"  标签: {r.get('tags', [])}")
            lines.append("")
        return "\n".join(lines)

    def _search_tags(self, tags):
        """标签搜索"""
        results = self.knowledge_searcher.search_by_tags(tags)
        if not results:
            return f"标签搜索 {tags}: 未找到结果"

        lines = [f"标签搜索 {tags}: 找到 {len(results)} 个文件", "=" * 50]
        for r in results:
            lines.append(f"  文件: {r['file']}  标题: {r.get('title', 'N/A')}  标签: {r.get('tags', [])}")
        return "\n".join(lines)

    def _search_semantic(self, query):
        """语义搜索"""
        results = self.knowledge_searcher.semantic_search(query)
        if not results:
            return f"语义搜索 '{query}': 未找到结果"

        lines = [f"语义搜索 '{query}': 找到 {len(results)} 个文件", "=" * 50]
        for r in results:
            relevance = r.get('relevance', 0)
            lines.append(f"  [{relevance:.0%}] {r['file']}")
            lines.append(f"  标题: {r.get('title', 'N/A')}")
            lines.append(f"  摘要: {r.get('snippet', '')[:120]}")
            lines.append("")
        return "\n".join(lines)

    # -----------------------------------------------------------------
    # chat — 交互式对话
    # -----------------------------------------------------------------
    def chat(self):
        """交互式对话"""
        print(self.greet())
        print("交互模式启动中...")
        print("输入 'quit' 或 'exit' 退出")
        print("输入 'help' 查看可用命令")
        print("=" * 60)

        while True:
            try:
                user_input = input(f"{self.name} > ").strip()

                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n再见昌叔！有需要随时找我！")
                    break

                if not user_input:
                    continue

                # 特殊命令
                if user_input.lower() == 'help':
                    chat_help = """
可用命令:
  help           - 显示帮助
  status         - 查看状态
  reload         - 重新加载配置
  diagnose       - 系统诊断
  model-stats    - 显示模型性能统计
  quit/exit      - 退出
  其他输入       - 提问
"""
                    print(chat_help)
                    continue

                if user_input.lower() == 'status':
                    print(self.status())
                    continue

                if user_input.lower() == 'reload':
                    print(self.reload_config())
                    continue

                if user_input.lower() == 'diagnose':
                    print(self.diagnose())
                    continue

                if user_input.lower() == 'model-stats':
                    all_stats = self.model_monitor.get_all_stats()
                    if all_stats:
                        for model_name, stats in all_stats.items():
                            print(f"  {model_name}: "
                                  f"调用{stats['total_calls']}次, "
                                  f"平均响应{stats['avg_response_time']:.2f}s, "
                                  f"总Token{stats['total_tokens']}")
                    else:
                        print("暂无模型性能数据")
                    continue

                # 普通问题
                print(self.ask(user_input))
                print()

            except KeyboardInterrupt:
                print("\n\n再见昌叔！有需要随时找我！")
                break
            except EOFError:
                print("\n\n再见昌叔！有需要随时找我！")
                break
            except Exception as e:
                print(f"\n错误: {e}")
                print("请重试或输入 'quit' 退出\n")


# =====================================================================
# 主函数
# =====================================================================
def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='昌叔专属软件开发助手 v3.0.0',
    )
    parser.add_argument('command', nargs='?', help='主命令')
    parser.add_argument('subcommand', nargs='?', help='子命令')
    parser.add_argument('extra_args', nargs='*', help='额外参数')
    parser.add_argument('--config', help='配置文件路径')
    parser.add_argument('--file', help='文件路径')
    parser.add_argument('--question', help='问题')

    args = parser.parse_args()
    assistant = ChangshuAssistant(args.config)

    if not args.command:
        print(assistant.greet())
        print(assistant.help())
        return

    command = args.command.lower()
    subcmd = args.subcommand
    extra = args.extra_args or []

    if command == 'help':
        print(assistant.help())

    elif command == 'chat':
        assistant.chat()

    elif command == 'ask':
        question = args.question or (subcmd or '')
        if subcmd and extra:
            question = subcmd + ' ' + ' '.join(extra)
        if not question:
            print("错误: 请提供问题，例如: changshu-assistant ask 如何优化达梦数据库查询？")
        else:
            print(assistant.ask(question))

    elif command == 'review':
        file_path = args.file or subcmd or (extra[0] if extra else None)
        if file_path:
            print(assistant.review(file_path))
        else:
            print("错误: 请指定要审查的文件路径，例如: changshu-assistant review app.py")

    elif command == 'diagnose':
        print(assistant.diagnose())

    elif command == 'status':
        print(assistant.status())

    elif command == 'sql':
        print(assistant.cmd_sql(subcmd, extra))

    elif command == 'scan':
        print(assistant.cmd_scan(subcmd, extra))

    elif command == 'search':
        print(assistant.cmd_search(subcmd, extra))

    elif command == 'skill':
        skill_name = args.file or subcmd or (extra[0] if extra else None)
        if skill_name:
            print(assistant.view_skill(skill_name))
        else:
            print("错误: 请指定skill名称")

    elif command == 'run':
        skill_name = args.file or subcmd or (extra[0] if extra else None)
        if skill_name:
            run_extra = extra[1:] if len(extra) > 1 else []
            print(assistant.run_skill(skill_name, run_extra))
        else:
            print("错误: 请指定skill名称")

    else:
        print(f"未知命令: {command}")
        print(assistant.help())


if __name__ == '__main__':
    main()
