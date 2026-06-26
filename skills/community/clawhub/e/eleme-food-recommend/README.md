# 饿了么外卖推荐 Skill

根据用户的饭点设置和口味偏好，在饭点前推荐附近外卖店铺的菜品。

## 功能

- 设置用户饭点（早餐、午餐、晚餐时间）
- 设置口味偏好（清淡、重口、微辣、中辣等）
- 设置每日推荐菜品数量
- 根据定位获取附近外卖店
- 智能推荐符合口味的菜品

## 目录结构

```
eleme-food-recommend/
├── SKILL.md              # 技能配置
├── README.md             # 说明文档
└── scripts/
    ├── main.py           # 主入口
    ├── config_manager.py # 配置管理
    ├── eleme_api.py     # 饿了么API
    └── recommend.py      # 推荐逻辑
```

## 使用

### 设置用户配置

```bash
# 基本设置
python scripts/main.py set-config --cookie "your_eleme_cookie"

# 完整设置（包含定位）
python scripts/main.py set-config \
  --cookie "your_eleme_cookie" \
  --breakfast "07:30" \
  --lunch "11:30" \
  --dinner "18:30" \
  --flavor "清淡" \
  --count 3 \
  --latitude 39.90 \
  --longitude 116.40 \
  --address "北京市朝阳区"
```

### 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| --cookie | 饿了么Cookie（必须） | 从浏览器F12获取 |
| --breakfast | 早餐时间 | 07:30 |
| --lunch | 午餐时间 | 11:30 |
| --dinner | 晚餐时间 | 18:30 |
| --flavor | 口味偏好 | 清淡/微辣/中辣/辣/重口/甜/酸/不限 |
| --count | 推荐数量 | 3 |
| --latitude | 纬度 | 39.90 |
| --longitude | 经度 | 116.40 |
| --address | 地址描述 | 北京市朝阳区 |

### 查看配置

```bash
python scripts/main.py show-config
```

### 获取推荐

```bash
python scripts/main.py recommend
```

### 查看饭点状态

```bash
python scripts/main.py status
```

## 如何获取饿了么Cookie

1. 在浏览器中打开饿了么官网 (https://www.ele.me)
2. 登录账号
3. 按 F12 打开开发者工具
4. 切换到 Network（网络）标签
5. 刷新页面，点击任意请求
6. 在 Request Headers 中找到 Cookie，复制其值

## 发布到ClawHub

```bash
# 安装 clawhub CLI（如果未安装）
npm i -g clawhub

# 登录
clawhub login

# 进入技能目录
cd ~/.openclaw/skills

# 发布（需要先复制技能到该目录）
# 复制技能
cp -r /path/to/eleme-food-recommend ~/.openclaw/skills/

# 发布
clawhub publish eleme-food-recommend --slug eleme-food-recommend --name eleme-food-recommend --version 1.0.0 --changelog "Initial release"

# 如果发布失败，尝试
clawhub undelete eleme-food-recommend
```

## 注意事项

- Cookie 是必须的，否则无法获取附近店铺
- 建议设置定位信息以获取更准确的推荐
- 推荐在饭点前30分钟内使用 recommend 命令获取推荐
