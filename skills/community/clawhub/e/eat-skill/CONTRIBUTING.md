# 贡献指南

欢迎贡献你常去的餐馆！把一家店变成 AI Skill，让更多人知道这家好店。

## 最快的方式（3 分钟）

### 1. Fork 仓库

点右上角 Fork。

### 2. 创建餐馆目录

```bash
mkdir restaurants/你的餐馆英文名
```

目录名规范：全小写，用连字符分隔，比如 `laowang-bbq`、`uncle-chen-noodle`。

### 3. 填写餐馆信息

复制模板并填写：

```bash
cp templates/restaurant-info.yaml restaurants/你的餐馆英文名/restaurant-info.yaml
```

打开文件，填上餐馆信息。带 `*` 的是必填，其他能填多少填多少。

### 4. 生成 SKILL.md

```bash
node generator/generate.mjs \
  --input restaurants/你的餐馆英文名/restaurant-info.yaml \
  --output restaurants/你的餐馆英文名/SKILL.md
```

也可以直接手写 `SKILL.md`，不用生成器也行。

### 5. 更新餐馆列表

在 `restaurants/README.md` 的表格里加一行你的餐馆。

### 6. 提 PR

```bash
git add .
git commit -m "feat: add 餐馆名"
git push origin your-branch
```

然后在 GitHub 上提 Pull Request。

## 也可以不写代码

如果你不想折腾命令行，可以直接在 GitHub 上：

1. 点 `restaurants/` 目录
2. 点 "Add file" → "Create new file"
3. 文件名填 `你的餐馆名/SKILL.md`
4. 参考已有的餐馆格式，手写一份
5. 提 PR

格式不完美没关系，我们会帮你调整。

## 也可以用 Issue

不想写文件？直接开个 Issue，标题写"新增餐馆：XXX"，把店名、地址、营业时间、推荐菜写上就行。我们来帮你生成。

## SKILL.md 质量检查

提 PR 前，确认你的 `SKILL.md` 至少包含：

- 餐馆名称
- 地址
- 营业时间
- 品类（什么类型的店）
- 至少一道推荐菜

以下信息越全越好：

- 人均消费
- 怎么去（交通/地标）
- 外卖信息
- 排队/预约方式
- 氛围描述
- 适合场景标签

## 规范

### 信息真实性

- **只贡献你真实去过的店**，不要从网上抄
- 价格以实际到店为准，标注"参考价"即可
- 不需要把整个菜单都列出来，推荐几个招牌就行

### 语气风格

- 像给朋友推荐一样，自然、实在
- 不搞营销文案，不堆形容词
- 可以有个人感受，比如"面皮劲道，蘸醋绝了"

### 不接受

- 广告软文
- 虚假信息
- 不带地址的推荐（至少告诉大家在哪个城市哪个区）

## 有问题？

开 Issue 聊，或者 PR 里讨论。