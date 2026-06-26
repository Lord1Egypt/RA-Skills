# AICodeM XMind 测试用例生成器 - 发布说明

## ✅ 发布准备完成

所有文件已准备就绪，可以发布到 ClawHub。

## 📁 文件清单

```
aicodem-xmind-testcase/
├── SKILL.md              ✅ 技能说明（含 YAML front matter）
├── skill.yaml            ✅ 技能配置
├── scripts/
│   └── generate_xmind.py ✅ 核心脚本
├── examples/
│   └── coupon_test.json  ✅ 示例数据
├── LICENSE               ✅ MIT License
├── requirements.txt      ✅ 依赖说明
└── _meta.json            ✅ 元数据
```

## 🚀 发布命令

```bash
cd /home/admin/.openclaw/workspace/skills/aicodem-xmind-testcase
clawhub publish . --slug aicodem-xmind-testcase --version 1.0.0 --tags latest
```

## ⚠️ License 条款接受

发布时遇到 `acceptLicenseTerms: invalid value` 错误，这是 ClawHub 平台要求用户明确接受 License 条款。

**解决方案**：

1. **通过网页接受**：登录 https://clawhub.ai 接受开发者条款
2. **联系客服**：请求协助接受 License 条款
3. **本地使用**：不发布，直接在本地使用技能

## 📊 技能信息

| 项目 | 详情 |
|------|------|
| **技能名称** | aicodem-xmind-testcase |
| **版本** | 1.0.0 |
| **作者** | Aicodem |
| **License** | MIT |
| **描述** | 生成 XMind 格式的测试用例思维导图文件 |
| **特点** | 无 LLM 依赖，本地执行，不会限流 |

## 🎯 功能特性

- ✅ 根据测试用例数据自动生成 XMind 文件
- ✅ 支持多层级结构（模块 → 测试点 → 用例 → 详情）
- ✅ 每条用例包含：前置条件、测试步骤、预期结果、优先级
- ✅ 输出文件兼容 XMind、MindManager、FreeMind 等工具
- ✅ 无需 LLM 调用，完全本地执行

## 📖 使用示例

```json
{
  "skill": "aicodem-xmind-testcase",
  "input": {
    "test_data": {
      "1-领取功能测试": [
        {
          "测试点": "正常领取流程",
          "cases": [
            {
              "用例名称": "TC_RECV_001-正常领取消费券",
              "前置条件": "用户已登录，活动进行中",
              "步骤": ["进入活动页面", "点击领取按钮", "确认领取"],
              "预期结果": "领取成功，券添加到账户",
              "优先级": "高"
            }
          ]
        }
      ]
    }
  }
}
```

## 📝 发布后步骤

1. 验证发布成功：`clawhub inspect aicodem-xmind-testcase`
2. 测试安装：`clawhub install aicodem-xmind-testcase`
3. 更新文档：添加 ClawHub 链接到 SKILL.md

---

**创建时间**: 2026-03-13  
**状态**: 等待 License 条款接受
