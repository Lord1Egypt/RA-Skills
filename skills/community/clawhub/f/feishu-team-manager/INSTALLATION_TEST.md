# 安装验证指南

## 目的
验证从ClawHub安装feishu-team-manager技能的完整流程，确保新用户能够正确安装和使用。

## 测试环境
- OpenClaw版本: >= 2026.3.20
- 操作系统: Linux
- 技能版本: 2.3.1

## 完整安装流程验证

### 步骤1: 从ClawHub安装技能
```bash
# 安装技能
clawhub install feishu-team-manager

# 验证安装
clawhub list | grep feishu-team-manager
```

**预期结果**: 显示 `feishu-team-manager  2.3.1`

### 步骤2: 验证技能文件结构
```bash
# 检查技能目录
ls -la ~/.openclaw/workspace/skills/feishu-team-manager/

# 检查核心文件
ls -la ~/.openclaw/workspace/skills/feishu-team-manager/scripts/
```

**预期结果**:
- `index.js` 存在且可执行
- `scripts/` 目录包含三个Python脚本
- `assets/` 目录包含模板和图片

### 步骤3: 验证技能激活
技能安装后需要激活才能使用。激活方法：
1. 在OpenClaw对话中提及技能关键词
2. 或直接运行安装脚本

**激活测试**:
```bash
# 检查技能是否在可用技能列表中
openclaw skills list | grep feishu
```

### 步骤4: 基本功能测试

#### 4.1 环境检查脚本
```bash
cd ~/.openclaw/workspace/skills/feishu-team-manager
python3 scripts/check_env.py
```

**预期结果**: 返回JSON格式的环境检查结果

#### 4.2 招聘脚本测试（模拟）
```bash
# 测试招聘脚本（不实际创建）
python3 scripts/recruit_agent.py test_agent hr_template
```

**预期结果**: 显示招聘成功提示

### 步骤5: 文档完整性检查
1. SKILL.md 文件存在且格式正确
2. CHANGELOG.md 包含最新版本信息
3. PUBLISH_GUIDE.md 提供发布指南
4. 图片链接可访问

```bash
# 检查图片链接
curl -I "https://gitee.com/noahtao/wordpress-auto-publisher/raw/main/images/wechat_donate.png"
curl -I "https://gitee.com/noahtao/wordpress-auto-publisher/raw/main/images/alipay_donate.jpg"
```

**预期结果**: HTTP 200 OK

## 故障排除

### 常见问题1: 技能安装失败
**症状**: `clawhub install` 失败
**解决方案**:
1. 检查网络连接
2. 验证ClawHub账户登录状态: `clawhub whoami`
3. 尝试强制安装: `clawhub install feishu-team-manager --force`

### 常见问题2: 技能无法激活
**症状**: 技能安装后无法使用
**解决方案**:
1. 检查技能目录权限
2. 重启OpenClaw Gateway: `openclaw gateway restart`
3. 验证技能配置文件: 检查 `~/.openclaw/openclaw.json` 中的技能配置

### 常见问题3: 图片无法显示
**症状**: 赞赏码图片显示为占位符
**解决方案**:
1. 检查网络连接，确保可以访问Gitee
2. 验证图片URL是否正确
3. 考虑使用其他图床服务

## 自动化测试脚本

创建自动化测试脚本 `test_installation.sh`:

```bash
#!/bin/bash
echo "=== feishu-team-manager 安装验证测试 ==="

# 1. 检查技能是否已安装
echo "1. 检查技能安装状态..."
clawhub list | grep feishu-team-manager
if [ $? -eq 0 ]; then
    echo "✅ 技能已安装"
else
    echo "❌ 技能未安装"
    exit 1
fi

# 2. 检查文件结构
echo "2. 检查文件结构..."
SKILL_DIR="$HOME/.openclaw/workspace/skills/feishu-team-manager"
if [ -d "$SKILL_DIR" ]; then
    echo "✅ 技能目录存在"
    ls -la "$SKILL_DIR" | head -10
else
    echo "❌ 技能目录不存在"
    exit 1
fi

# 3. 检查核心脚本
echo "3. 检查核心脚本..."
for script in index.js scripts/recruit_agent.py scripts/bind_bot.py scripts/check_env.py; do
    if [ -f "$SKILL_DIR/$script" ]; then
        echo "✅ $script 存在"
    else
        echo "❌ $script 不存在"
    fi
done

# 4. 检查图片链接
echo "4. 检查图片链接..."
for url in \
    "https://gitee.com/noahtao/wordpress-auto-publisher/raw/main/images/wechat_donate.png" \
    "https://gitee.com/noahtao/wordpress-auto-publisher/raw/main/images/alipay_donate.jpg"
do
    if curl -s -I "$url" | grep -q "200 OK"; then
        echo "✅ $url 可访问"
    else
        echo "⚠  $url 访问异常"
    fi
done

echo "=== 测试完成 ==="
```

## 验证结果记录

| 测试项目 | 状态 | 备注 |
|---------|------|------|
| ClawHub安装 | ✅ | 技能可正常安装 |
| 文件结构 | ✅ | 所有必需文件存在 |
| 脚本可执行性 | ✅ | Python脚本可正常运行 |
| 文档完整性 | ✅ | SKILL.md、CHANGELOG.md完整 |
| 图片可访问性 | ✅ | Gitee图片链接正常 |
| 技能激活 | ✅ | 技能可正常激活使用 |

## 后续改进建议

1. **添加更详细的安装说明**：在SKILL.md中补充从ClawHub安装的具体步骤
2. **创建快速开始指南**：提供5分钟快速上手指南
3. **添加视频教程**：录制安装和使用视频
4. **建立用户反馈渠道**：在技能页面添加反馈链接

---
**验证时间**: 2026-04-23
**验证版本**: 2.3.1
**验证环境**: OpenClaw 标准环境