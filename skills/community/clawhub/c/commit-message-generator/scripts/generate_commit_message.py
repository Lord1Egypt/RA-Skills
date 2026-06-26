#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git 提交信息生成器
根据代码变更内容自动生成符合 Conventional Commits 规范的提交信息
"""

import re
import sys
import json
from datetime import datetime

# Conventional Commits 类型定义
COMMIT_TYPES = {
    'feat': '新功能',
    'fix': '修复 Bug',
    'docs': '文档更新',
    'style': '代码格式（不影响功能）',
    'refactor': '重构（既不是新功能也不是 Bug 修复）',
    'perf': '性能优化',
    'test': '测试相关',
    'chore': '构建过程或辅助工具变动',
    'ci': 'CI 配置',
    'build': '构建系统',
    'revert': '回滚'
}

# 常见模块范围
COMMON_SCOPES = [
    'algorithm', 'ui', 'api', 'database', 'config',
    'test', 'docs', 'build', 'deploy', 'core',
    'module', 'service', 'controller', 'model', 'view'
]

def analyze_change_type(diff_text: str) -> str:
    """分析变更类型"""
    diff_lower = diff_text.lower()
    
    # 新功能特征
    if any(kw in diff_lower for kw in ['新增', '添加', 'add', 'new', 'create', 'introduce']):
        if any(kw in diff_lower for kw in ['功能', 'feature', 'support']):
            return 'feat'
    
    # Bug 修复特征
    if any(kw in diff_lower for kw in ['修复', 'fix', 'bug', 'issue', '错误', '问题', '解决']):
        return 'fix'
    
    # 文档特征
    if any(kw in diff_lower for kw in ['文档', 'doc', 'readme', 'comment', '注释']):
        return 'docs'
    
    # 重构特征
    if any(kw in diff_lower for kw in ['重构', 'refactor', '整理', '清理', 'cleanup']):
        return 'refactor'
    
    # 性能优化特征
    if any(kw in diff_lower for kw in ['性能', 'perf', '优化', 'optimize', '加速']):
        return 'perf'
    
    # 测试特征
    if any(kw in diff_lower for kw in ['测试', 'test', 'unit', '用例']):
        return 'test'
    
    # 代码格式特征
    if any(kw in diff_lower for kw in ['格式', 'format', '缩进', '空格', 'lint']):
        return 'style'
    
    # 默认为 chore
    return 'chore'

def extract_scope(diff_text: str) -> str:
    """提取影响范围（模块名）"""
    # 尝试从文件路径提取模块名
    file_pattern = r'(?:diff --git|修改文件|文件：)\s*[^\s]+/([^\s/]+)'
    matches = re.findall(file_pattern, diff_text)
    if matches:
        return matches[0]
    
    # 尝试从常见模块名匹配
    for scope in COMMON_SCOPES:
        if scope.lower() in diff_text.lower():
            return scope
    
    # 尝试从类名/函数名提取
    class_pattern = r'(?:class|def|function)\s+([A-Za-z_][A-Za-z0-9_]*)'
    matches = re.findall(class_pattern, diff_text)
    if matches:
        return matches[0].lower()
    
    return 'core'

def generate_subject(change_type: str, scope: str, description: str) -> str:
    """生成主题行（50 字符以内）"""
    # 清理描述，去除多余空格
    description = ' '.join(description.split())
    
    # 截断到合适长度（类型 + 范围 + 描述 ≈ 50 字符）
    max_desc_len = 50 - len(change_type) - len(scope) - 3
    if len(description) > max_desc_len:
        description = description[:max_desc_len-2] + '...'
    
    return f"{change_type}({scope}): {description}"

def generate_body(diff_text: str, change_type: str) -> str:
    """生成详细正文"""
    body_lines = []
    
    # 分析变更内容，提取关键点
    lines = diff_text.split('\n')
    changes = []
    
    for line in lines:
        line = line.strip()
        if line.startswith('+') and not line.startswith('+++'):
            # 新增内容
            changes.append(('新增', line[1:50]))  # 限制长度
        elif line.startswith('-') and not line.startswith('---'):
            # 删除内容
            changes.append(('删除', line[1:50]))
        elif line.startswith('修改') or line.startswith('更新'):
            changes.append(('修改', line[2:50]))
    
    # 生成变更说明
    if changes:
        body_lines.append('')
        for action, content in changes[:5]:  # 最多 5 条
            if content.strip():
                body_lines.append(f"- {action}: {content.strip()}")
    
    # 添加影响说明
    body_lines.append('')
    if change_type == 'feat':
        body_lines.append("影响：新功能，不影响现有功能")
    elif change_type == 'fix':
        body_lines.append("影响：修复问题，建议尽快合并")
    elif change_type == 'refactor':
        body_lines.append("影响：代码重构，功能不变")
    elif change_type == 'perf':
        body_lines.append("影响：性能提升，建议测试验证")
    else:
        body_lines.append("影响：详见变更内容")
    
    return '\n'.join(body_lines)

def parse_user_input(user_input: str) -> dict:
    """解析用户输入，提取关键信息"""
    result = {
        'description': '',
        'issue_id': None,
        'breaking_change': False,
        'co_authors': []
    }
    
    # 提取 Issue 号
    issue_pattern = r'(?:#|issue-?|需求)[- ]?(\d+)'
    issue_match = re.search(issue_pattern, user_input, re.IGNORECASE)
    if issue_match:
        result['issue_id'] = issue_match.group(1)
    
    # 提取破坏性变更标记
    if any(kw in user_input for kw in ['破坏性', 'breaking', '不兼容', 'major']):
        result['breaking_change'] = True
    
    # 提取联合作者
    author_pattern = r'(?:co-authored-by|联合作者)[:\s]+([^\n]+)'
    author_matches = re.findall(author_pattern, user_input, re.IGNORECASE)
    result['co_authors'] = [a.strip() for a in author_matches]
    
    # 剩余部分作为描述
    result['description'] = re.sub(issue_pattern, '', user_input, flags=re.IGNORECASE)
    result['description'] = re.sub(author_pattern, '', result['description'], flags=re.IGNORECASE)
    result['description'] = result['description'].strip(' -:')
    
    return result

def generate_commit_message(user_input: str, diff_text: str = '') -> str:
    """生成完整的提交信息"""
    
    # 合并用户输入和 diff
    full_text = user_input + '\n' + diff_text
    
    # 解析用户输入
    parsed = parse_user_input(user_input)
    
    # 分析变更类型和范围
    change_type = analyze_change_type(full_text)
    scope = extract_scope(full_text)
    
    # 使用用户描述或自动生成
    description = parsed['description'] if parsed['description'] else f"更新{scope}模块"
    
    # 生成主题行
    subject = generate_subject(change_type, scope, description)
    
    # 生成正文
    body = generate_body(full_text, change_type)
    
    # 添加 Issue 引用
    footer = ''
    if parsed['issue_id']:
        footer = f"\nCloses #{parsed['issue_id']}"
    
    # 添加破坏性变更说明
    if parsed['breaking_change']:
        footer += "\n\nBREAKING CHANGE: 此变更包含不兼容的 API 修改"
    
    # 添加联合作者
    for author in parsed['co_authors']:
        footer += f"\nCo-authored-by: {author}"
    
    # 组合完整提交信息
    commit_message = subject + body + footer
    
    return commit_message

def format_output(commit_message: str, change_type: str) -> str:
    """格式化输出"""
    type_desc = COMMIT_TYPES.get(change_type, '其他')
    
    output = f"""# 📝 Git 提交信息

**生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**变更类型：** {change_type} ({type_desc})

---

## 提交信息

```
{commit_message}
```

---

## 使用说明

### 直接复制使用

```bash
git commit -m "主题行" -m "正文内容"
```

### 或使用编辑器

```bash
git commit
# 粘贴上述完整内容
```

---

## Conventional Commits 规范

| 类型 | 说明 | 使用场景 |
|------|------|----------|
| feat | 新功能 | 新增功能特性 |
| fix | 修复 Bug | 修复问题 |
| docs | 文档 | 文档更新 |
| style | 格式 | 代码格式调整 |
| refactor | 重构 | 代码重构 |
| perf | 性能 | 性能优化 |
| test | 测试 | 测试相关 |
| chore | 杂项 | 构建/工具等 |

---

## 自定义建议

如需调整提交信息，可修改：
- **主题行**：保持 50 字符以内，清晰描述变更
- **正文**：说明为什么修改，而不是修改了什么
- **Footer**：关联 Issue、破坏性变更等

---

**提示：** 可以粘贴 `git diff` 输出获取更准确的建议
"""
    
    return output

def main():
    if len(sys.argv) < 2:
        print(json.dumps({'error': '请提供变更描述或 git diff 内容'}, ensure_ascii=False))
        sys.exit(1)
    
    user_input = ' '.join(sys.argv[1:])
    commit_msg = generate_commit_message(user_input)
    change_type = analyze_change_type(user_input)
    output = format_output(commit_msg, change_type)
    
    print(output)

if __name__ == '__main__':
    main()
