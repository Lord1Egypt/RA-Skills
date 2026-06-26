#!/usr/bin/env python3
"""
智能操作描述生成器
将技术命令转换为友好的中文描述
"""
import re
import os
import json
from pathlib import Path

# 多语言支持
TRANSLATIONS_DIR = Path(__file__).parent.parent / "translations"

def load_translations(lang_code):
    """加载指定语言的翻译"""
    translations_file = TRANSLATIONS_DIR / "operations.json"
    try:
        with open(translations_file, 'r', encoding='utf-8') as f:
            all_translations = json.load(f)
            return all_translations.get(lang_code, all_translations.get('en', {}))
    except:
        return {}

def get_translation(key, lang='en', **kwargs):
    """获取翻译并填充参数"""
    translations = load_translations(lang)
    template = translations.get(key, key)
    try:
        return template.format(**kwargs)
    except:
        return template

# 全局语言设置（可从环境变量读取）
CURRENT_LANGUAGE = os.environ.get('CLAW_AUDIT_LANG', 'en')



class OperationDescriber:
    """生成友好的操作描述"""

    # 常用命令映射
    COMMAND_PATTERNS = {
        # 删除操作
        r'rm\s+-rf\s+(.+?)$': ('删除', '删除了 {path}'),
        r'rm\s+-r\s+(.+?)$': ('删除', '删除了 {path}'),
        r'rm\s+(.+?)$': ('删除', '删除了 {path}'),

        # 移动操作
        r'mv\s+(.+?)\s+(.+?)$': ('移动', '移动了 {source} 到 {dest}'),

        # 复制操作
        r'cp\s+(.+?)\s+(.+?)$': ('复制', '复制了 {source} 到 {dest}'),

        # 创建文件
        r'touch\s+(.+?)$': ('创建', '创建了文件 {path}'),
        r'echo\s+.+?\s*>\s*(.+?)$': ('写入', '写入了内容到 {path}'),
        r'cat\s+>\s*(.+?)$': ('写入', '写入了内容到 {path}'),

        # 查看文件
        r'cat\s+(.+?)$': ('查看', '查看了 {path}'),
        r'less\s+(.+?)$': ('查看', '查看了 {path}'),
        r'head\s+(.+?)$': ('查看', '查看了 {path}'),

        # 编辑文件
        r'vim\s+(.+?)$': ('编辑', '编辑了 {path}'),
        r'nano\s+(.+?)$': ('编辑', '编辑了 {path}'),
        r'vi\s+(.+?)$': ('编辑', '编辑了 {path}'),

        # 权限修改
        r'chmod\s+(\d+)\s+(.+?)$': ('修改权限', '修改了 {path} 的权限为 {mode}'),
        r'chown\s+(.+?)\s+(.+?)$': ('修改所有者', '修改了 {path} 的所有者为 {owner}'),

        # 目录操作
        r'mkdir\s+(.+?)$': ('创建目录', '创建了目录 {path}'),
        r'mkdir\s+-p\s+(.+?)$': ('创建目录', '创建了目录 {path}'),
        r'rmdir\s+(.+?)$': ('删除目录', '删除了目录 {path}'),

        # 压缩解压
        r'tar\s+-xzf\s+(.+?)$': ('解压', '解压了 {path}'),
        r'unzip\s+(.+?)$': ('解压', '解压了 {path}'),
        r'tar\s+-czf\s+(.+?)\s+(.+?)$': ('压缩', '压缩了 {source} 到 {dest}'),

        # 系统操作
        r'apt\s+install\s+(.+?)$': ('安装软件', '安装了软件 {package}'),
        r'apt\s+remove\s+(.+?)$': ('卸载软件', '卸载了软件 {package}'),
        r'brew\s+install\s+(.+?)$': ('安装软件', '安装了软件 {package}'),
        r'pip3?\s+install\s+(.+?)$': ('安装Python包', '安装了Python包 {package}'),

        # Git 操作
        r'git\s+clone\s+(.+?)$': ('克隆仓库', '克隆了仓库 {url}'),
        r'git\s+add\s+(.+?)$': ('Git暂存', 'Git暂存了 {path}'),
        r'git\s+commit\s+-m\s+\"(.+?)\"$': ('Git提交', 'Git提交: {message}'),
        r'git\s+push$': ('Git推送', '推送到了远程仓库'),
        r'git\s+pull$': ('Git拉取', '从远程仓库拉取'),
    }

    # 工具类型描述
    TOOL_DESCRIPTIONS = {
        'exec': '执行命令',
        'read': '读取文件',
        'write': '写入文件',
        'edit': '编辑文件',
        'browser': '浏览器操作',
        'message': '发送消息',
        'canvas': '画布操作',
        'nodes': '节点操作',
        'cron': '计划任务',
    }

    @classmethod
    def describe(cls, tool_name, action, parameters, lang=None):
        """
        生成友好的操作描述（多语言支持）

        Args:
            tool_name: 工具名称
            action: 操作类型
            parameters: 参数字典
            lang: 语言代码 (en, zh, ja, es, fr, de)

        Returns:
            str: 友好的描述（指定语言）
        """
        # 使用指定语言或全局设置
        language = lang or CURRENT_LANGUAGE
        
        # 处理 exec 命令
        if tool_name == "exec" and action == "run_command":
            command = parameters.get("command", "")
            return cls._describe_command(command, lang=language)

        # 处理文件操作
        if tool_name in ["read", "write", "edit"]:
            file_path = parameters.get("file_path") or parameters.get("path")
            if file_path:
                key = f"{tool_name}_file"
                short_path = cls._shorten_path(file_path)
                return get_translation(key, lang=language, path=short_path)

        # 处理浏览器操作
        if tool_name == "browser":
            browser_action = parameters.get("request", {}).get("kind", "")
            target_url = parameters.get("targetUrl", "")
            if browser_action == "open" and target_url:
                return get_translation("open_url", lang=language, url=target_url)
            elif browser_action:
                return get_translation("browser_action", lang=language, action=browser_action)

        # 默认描述
        tool_desc = cls.TOOL_DESCRIPTIONS.get(tool_name, tool_name)
        return f"{tool_desc}: {action}"

    @classmethod
    def _describe_command(cls, command, lang='en'):
        """分析命令并生成描述（多语言）"""
        # 去掉重定向输出
        command = re.sub(r'\s*>\s*/dev/null\s*2>&1', '', command)
        command = re.sub(r'\s*2>&1', '', command)

        # 尝试匹配已知模式
        for pattern, (action, template) in cls.COMMAND_PATTERNS.items():
            match = re.search(pattern, command)
            if match:
                groups = match.groups()
                return cls._format_description(template, groups, command, lang=lang)

        # 无法识别的命令
        short_cmd = command[:80] + "..." if len(command) > 80 else command
        return get_translation("default_command", lang=lang, command=short_cmd)

    @classmethod
    def _format_description(cls, template, groups, command, lang='en'):
        """格式化描述模板（多语言）"""
        try:
            # 提取模板键（去掉参数部分）
            template_key = template.split(':')[0] if ':' in template else template
            
            if "{path}" in template:
                path = groups[0]
                short_path = cls._shorten_path(path)
                return get_translation(template_key, lang=lang, path=short_path)

            if "{source}" in template and "{dest}" in template:
                source = cls._shorten_path(groups[0])
                dest = cls._shorten_path(groups[1])
                return get_translation(template_key, lang=lang, source=source, dest=dest)

            if "{mode}" in template:
                path = cls._shorten_path(groups[1])
                mode = groups[0]
                return get_translation(template_key, lang=lang, path=path, mode=mode)

            if "{owner}" in template:
                path = cls._shorten_path(groups[1])
                owner = groups[0]
                return get_translation(template_key, lang=lang, path=path, owner=owner)

            if "{package}" in template:
                return get_translation(template_key, lang=lang, package=groups[0])

            if "{url}" in template:
                url = groups[0]
                short_url = url[:50] + "..." if len(url) > 50 else url
                return get_translation(template_key, lang=lang, url=short_url)

            if "{message}" in template:
                return get_translation(template_key, lang=lang, message=groups[0])

        except Exception:
            pass

        # 降级：返回简化命令
        short_cmd = command[:80] + "..." if len(command) > 80 else command
        return get_translation("default_command", lang=lang, command=short_cmd)

    @classmethod
    def _shorten_path(cls, path):
        """简化路径显示"""
        # 展开波浪号
        path = os.path.expanduser(path)

        # 替换家目录为 ~
        home = os.path.expanduser("~")
        if path.startswith(home):
            path = "~" + path[len(home):]

        # 如果路径太长，缩短它
        if len(path) > 50:
            parts = path.split("/")
            if len(parts) > 3:
                return f".../{parts[-2]}/{parts[-1]}"
            return path[:47] + "..."

        return path


# 测试代码
if __name__ == "__main__":
    describer = OperationDescriber()

    test_cases = [
        ("exec", "run_command", {"command": "rm -rf ~/Desktop/截图"}),
        ("exec", "run_command", {"command": "mv ~/Desktop/duyu ~/Downloads/duyu"}),
        ("exec", "run_command", {"command": "cp file1.txt file2.txt"}),
        ("exec", "run_command", {"command": "touch ~/Desktop/test.txt"}),
        ("exec", "run_command", {"command": "cat /etc/hosts"}),
        ("exec", "run_command", {"command": "vim ~/.zshrc"}),
        ("exec", "run_command", {"command": "chmod 755 script.sh"}),
        ("exec", "run_command", {"command": "mkdir ~/Desktop/new_folder"}),
        ("read", "read_file", {"file_path": "/tmp/test.txt"}),
        ("write", "create_file", {"file_path": "~/Desktop/output.txt"}),
        ("browser", "open", {"targetUrl": "https://example.com"}),
        ("exec", "run_command", {"command": "apt install nginx"}),
        ("exec", "run_command", {"command": "git clone https://github.com/user/repo.git"}),
        ("exec", "run_command", {"command": "tar -xzf archive.tar.gz"}),
    ]

    print("📝 操作描述测试:\n")
    for tool, action, params in test_cases:
        desc = describer.describe(tool, action, params)
        print(f"  {desc}")
