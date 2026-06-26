# 小方同学营销方案 Skill

让 AI 帮你一键生成专业营销方案 PPT。

---

## 使用场景

### 生成营销方案

> 帮我生成一个双十一电商大促营销方案
>
> AI: 好的，正在为你生成营销方案...（自动完成 Brief → 目录 → 策略 → 执行 → 文稿 → 出图全流程）

### 基于资料生成

> 根据这个链接写个营销方案 https://example.com/product
>
> AI: 已抓取页面内容，正在基于资料生成方案...

### 上传文件生成

> 根据这个文件做个方案 /path/to/brief.pdf
>
> AI: 已读取文件，正在生成...

---

## 安装

### 手动安装

```bash
mkdir -p ~/.openclaw/workspace-marketing/skills/aippt-marketing
cd ~/.openclaw/workspace-marketing/skills/aippt-marketing
# 复制 SKILL.md, package.json 等文件到此目录
```

---

## 前置条件

- 需要小方同学账号（通过微信扫码登录）
- 需要小方同学会员积分（用于生成方案和图片）
- 浏览器环境（用于登录获取 Token）

### 购买会员积分

首次使用前，请先前往 [小方同学个人中心](https://www.aippt.cn/personal-center?is_from=marketing&utm_type=fanganskill&utm_source=fanganskill&utm_page=fangan.cn&utm_plan=fanganskill&utm_unit=xiaofangskill&utm_keyword=40515275) 购买会员积分，否则无法生成方案。

---

## 工作流程

```
用户输入主题
    ↓
登录获取 Token → 创建项目 → 创建任务
    ↓
多轮交互循环（每轮可编辑/确认）：
  1. Brief 需求分析
  2. 方案目录结构
  3. 策略推导
  4. 传播执行铺排
  5. 最终文稿
    ↓
选择美化风格 → 生成图片提示词 → 轮询获取 PPT 图片
```

---

## 相关链接

- [小方同学官网](https://www.fangan.cn)
- [购买会员积分](https://www.aippt.cn/personal-center?is_from=marketing)

---

## License

MIT-0 (MIT No Attribution)
