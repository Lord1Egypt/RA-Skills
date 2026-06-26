# Execute-Verify-Report (EVR) - AI三步法工具 ✅

> 执行不是确认，验证不是可选，报告不是敷衍

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 问题

| AI说的 | 实际 | 问题 |
|--------|------|------|
| "我会做的" | 没做 | 只确认不执行 |
| "完成了" | 未验证 | 跳过验证步骤 |
| "搞定了" | 有报错 | 静默失败 |
| "已提交" | 文件未变 | 假成功 |

**EVR三步法彻底解决。**

## 三步法

| 步骤 | 含义 | 命令示例 |
|------|------|---------|
| 🔧 **Execute** | 实际执行 | `chmod 600 file` |
| ✅ **Verify** | 验证结果 | `stat -c "%a" file` → `600` |
| 📋 **Report** | 完整汇报 | "权限已修改: 644→600, 验证通过" |

## 快速开始

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/aptratcn/skill-evr.git
```

在AGENTS.md中添加：
```markdown
## EVR铁律
所有任务必须: Execute → Verify → Report
违反EVR = 严重错误
```

## License

MIT

---

**Created by 小白** 🤍  
GitHub: [@aptratcn](https://github.com/aptratcn)
