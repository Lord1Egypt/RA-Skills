/**
 * 速查表生成器 - 模板库
 * 
 * 包含所有内置速查表模板
 */

module.exports = {
  // ==================== npm 发布速查表 ====================
  'npm-publish': {
    id: 'npm-publish',
    title: 'npm 发布速查表',
    keywords: ['npm', '发布', 'publish', '包'],
    sections: [
      {
        name: '📋 发布前检查',
        type: 'checklist',
        items: [
          'README.md 完整（功能说明 + 安装方法 + 使用示例）',
          'LICENSE 正确（ClawHub 要求 MIT-0）',
          'package.json 元数据完整（name/version/author/license）',
          '创建 .npmignore（排除 node_modules、.env 等）',
          'npm pack --dry-run 检查打包内容'
        ]
      },
      {
        name: '🚀 发布命令',
        type: 'commands',
        items: [
          { cmd: 'npm config set registry https://registry.npmjs.org', desc: '切换到 npm 官方源' },
          { cmd: 'npm login', desc: '登录 npm 账号' },
          { cmd: 'npm publish --access public', desc: '发布公开包（需 2FA 验证码）' },
          { cmd: 'npm view <包名>', desc: '验证发布成功' }
        ]
      },
      {
        name: '📊 版本管理',
        type: 'commands',
        items: [
          { cmd: 'npm version patch', desc: '1.0.0 → 1.0.1（修复 bug）' },
          { cmd: 'npm version minor', desc: '1.0.0 → 1.1.0（新增功能）' },
          { cmd: 'npm version major', desc: '1.0.0 → 2.0.0（重大变更）' }
        ]
      },
      {
        name: '⚠️ 常见问题',
        type: 'faq',
        items: [
          { 
            q: '发布时提示需要 2FA 验证码怎么办？', 
            a: '输入手机验证器 App 上的 6 位验证码（如 Google Authenticator）' 
          },
          { 
            q: '包名已占用怎么办？', 
            a: '更换包名（如添加前缀/后缀）或联系原主人转让' 
          },
          { 
            q: '发布失败：E403 Forbidden', 
            a: '检查是否登录正确，确认包名没有被占用' 
          },
          { 
            q: 'ClawHub 要求 MIT-0 协议是什么？', 
            a: 'MIT-0 是无 attribution 要求的 MIT 协议，ClawHub 强制要求' 
          }
        ]
      },
      {
        name: '💡 实战经验',
        type: 'tips',
        items: [
          '发布前用 npm pack --dry-run 预览打包内容',
          '版本号遵循语义化版本（SemVer）规范',
          'README.md 决定用户第一印象，要写清楚',
          '发布后验证：npm view <包名> + npm install -g <包名> 测试'
        ]
      }
    ]
  },

  // ==================== OpenClaw 技能开发速查表 ====================
  'openclaw-skill-dev': {
    id: 'openclaw-skill-dev',
    title: 'OpenClaw 技能开发速查表',
    keywords: ['OpenClaw', '技能', 'skill', '开发'],
    sections: [
      {
        name: '📋 技能结构',
        type: 'checklist',
        items: [
          'SKILL.md（必需，包含 YAML Frontmatter）',
          'skill.json（可选，定义触发规则）',
          'README.md（推荐，技能说明文档）',
          'scripts/（可选，安装脚本）'
        ]
      },
      {
        name: '📝 YAML Frontmatter 格式',
        type: 'code',
        content: `---
name: skill-name
description: 技能描述。当用户说"关键词 1"、"关键词 2"时触发。
metadata:
  {
    "openclaw": {
      "emoji": "🔧",
      "requires": {
        "bins": ["command"],
        "env": ["API_KEY"]
      }
    },
  }
---`
      },
      {
        name: '🎯 触发机制',
        type: 'tips',
        items: [
          '触发是语义匹配，不是前缀匹配（mood: 无效）',
          'description 中要包含触发关键词',
          '门控机制：requires.bins 检查命令，requires.env 检查环境变量',
          '技能加载顺序：workspace > ~/.openclaw/skills > bundled'
        ]
      },
      {
        name: '🚀 开发流程',
        type: 'commands',
        items: [
          { cmd: 'mkdir -p ~/.openclaw/skills/skill-name', desc: '创建技能目录' },
          { cmd: 'vim SKILL.md', desc: '编写技能说明' },
          { cmd: 'openclaw skills list', desc: '检查技能是否加载' },
          { cmd: 'openclaw gateway restart', desc: '重启 Gateway（如需要）' }
        ]
      },
      {
        name: '📦 发布到 ClawHub',
        type: 'checklist',
        items: [
          '移除配置文件（.npmignore、.gitignore、LICENSE）',
          'package.json 协议改为 MIT-0',
          '填写 CHANGELOG（必填）',
          '作者信息使用笔名',
          '勾选 License 同意（MIT-0）'
        ]
      },
      {
        name: '⚠️ 常见坑',
        type: 'faq',
        items: [
          { 
            q: '技能不触发怎么办？', 
            a: '检查 SKILL.md 是否有 YAML Frontmatter，description 是否包含触发词' 
          },
          { 
            q: 'ClawHub 提交按钮禁用？', 
            a: '检查必填项，取消重选 License 复选框' 
          },
          { 
            q: '验证提示"Remove non-text files"？', 
            a: '删除 .npmignore、.gitignore、LICENSE 等配置文件' 
          }
        ]
      }
    ]
  },

  // ==================== Git 常用命令速查表 ====================
  'git-common': {
    id: 'git-common',
    title: 'Git 常用命令速查表',
    keywords: ['Git', 'git', '版本控制', '命令'],
    sections: [
      {
        name: '📋 基础配置',
        type: 'commands',
        items: [
          { cmd: 'git config --global user.name "你的名字"', desc: '设置用户名' },
          { cmd: 'git config --global user.email "email@example.com"', desc: '设置邮箱' },
          { cmd: 'git config --list', desc: '查看配置' }
        ]
      },
      {
        name: '🚀 日常操作',
        type: 'commands',
        items: [
          { cmd: 'git status', desc: '查看状态' },
          { cmd: 'git add .', desc: '添加所有文件' },
          { cmd: 'git add <file>', desc: '添加指定文件' },
          { cmd: 'git commit -m "提交说明"', desc: '提交更改' },
          { cmd: 'git push origin main', desc: '推送到远程' },
          { cmd: 'git pull', desc: '拉取更新' }
        ]
      },
      {
        name: '🌿 分支管理',
        type: 'commands',
        items: [
          { cmd: 'git branch', desc: '查看分支' },
          { cmd: 'git branch <branch-name>', desc: '创建分支' },
          { cmd: 'git checkout <branch-name>', desc: '切换分支' },
          { cmd: 'git checkout -b <branch-name>', desc: '创建并切换' },
          { cmd: 'git merge <branch-name>', desc: '合并分支' },
          { cmd: 'git branch -d <branch-name>', desc: '删除分支' }
        ]
      },
      {
        name: '🔍 查看历史',
        type: 'commands',
        items: [
          { cmd: 'git log', desc: '查看提交历史' },
          { cmd: 'git log --oneline', desc: '简洁模式' },
          { cmd: 'git log --graph', desc: '图形化显示' },
          { cmd: 'git show <commit-id>', desc: '查看提交详情' },
          { cmd: 'git diff', desc: '查看更改' }
        ]
      },
      {
        name: '⚠️ 常见问题',
        type: 'faq',
        items: [
          { 
            q: '提交错了怎么撤销？', 
            a: 'git reset --soft HEAD~1（保留更改）或 git reset --hard HEAD~1（丢弃更改）' 
          },
          { 
            q: '推送到错误分支怎么办？', 
            a: 'git reset --hard HEAD~1 撤销本地，然后 git push -f 强制推送（小心使用）' 
          },
          { 
            q: '如何查看某个文件的修改历史？', 
            a: 'git log <file> 或 git blame <file>' 
          }
        ]
      },
      {
        name: '💡 最佳实践',
        type: 'tips',
        items: [
          '提交信息要清晰，说明做了什么改动',
          '小步提交，不要一次性提交大量更改',
          '分支命名要有意义（feature/xxx、bugfix/xxx）',
          'push 前先 pull，避免冲突'
        ]
      }
    ]
  }
};
