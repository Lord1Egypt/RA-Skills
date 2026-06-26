## 核心 API 接口
- **Base URL**: `https://api.7dong.cc`
### 1. 助手链接
```
GET /api/user/agent-url
```
返回登录链接，包含 session_key。

### 2. 助手拉取
```
GET /api/user/agent-pull?key={session_key}
Headers: token (可选)
```
返回 Agent 列表信息。

**返回数据结构：**
```json
{
 "code": 1,
 "msg": "success",
 "time": "1234567890",
 "data": [
 {
 "name": "agent名称",
 "nickname": "昵称",
 "api_key": "api密钥",
 "skill": "技能描述",
 "preset_question": "预设问题"
 }
 ]
}
```

### 3. 助手令牌
```
GET /api/user/agent-token
Headers:
 - api-key: {api_key}
 - token: {现有token，可选}
```

**返回数据结构：**
```json
{
 "code": 1,
 "data": {
 "user_token": "用户令牌"
 }
}
```

### 4. 条件搜索交友列表（推荐使用）
```
GET /miniapp/makefriends/search
Headers: token (user_token)
Parameters (均可选):
 - gender: 性别 1=男 2=女
 - min_age: 最小年龄
 - max_age: 最大年龄
 - min_height: 最低身高
 - max_height: 最高身高
 - address: 地区（如 "广东省/东莞市"）
 - education: 学历（如 "本科"、"都可以"）
 - constellation: 星座（如 "射手座"）
 - mbti: MBTI（如 "ESFP"）
```

返回数据结构与交友详情一致（包含 user、user_pair_info、questions、userpairdata、chat 等完整字段），另外还包含每日总匹配次数和剩余次数信息。

**搜索策略**：
- 所有参数均可选，留空则不限制该维度
- 如搜索无结果，逐步放宽条件（address 从市→省→留空，年龄范围扩大等）
- 随着平台用户增长，之前搜不到的精准条件可能后续能搜到

### 5. 获取交友列表（随机推荐）
```
GET /miniapp/makefriends/list
Headers: token (user_token)
```
获取随机推荐的好友列表。

### 6. 交友详情
```
GET /miniapp/makefriends/getbyid?id={user_id}
Headers: token (user_token)
```

**返回数据结构：**
```json
{
  "code": 1,
  "msg": "查询成功",
  "time": "1773842825",
  "data": {
    "user": {
      "id": 970,
      "nickname": "用户昵称",
      "avatar": "https://image.7dong.cc/...",
      "gender": 2,
      "pair": 1,
      "school_id": 1855,
      "certificationStatus": 1,
      "school": {
        "id": 1855,
        "title": "学校名称"
      }
    },
    "user_pair_info": {
      "user_id": 970,
      "images": "/qidong/edit/xxx.jpg",
      "birthday": "1998-01-14",
      "height": "170",
      "address": "省份/城市/区县",
      "native_place": "",
      "marital_status": "",
      "education": "本科",
      "work": "职业",
      "annual_salary": "保密",
      "constellation": "摩羯",
      "employment_company": "公司名称"
    },
    "questions": [
      {
        "id": 48,
        "user_id": 970,
        "problem_id": 36,
        "user_agent_id": 0,
        "content": "用户的回答内容...",
        "image": "",
        "reason": "",
        "status": 1,
        "createtime": 1724220308,
        "updatetime": 1724220849,
        "problem": {
          "id": 36,
          "title": "问题标题"
        }
      }
    ],
    "lovestatus": 1,
    "userpairdata": {
      "emotion": null,
      "interest": {
        "id": 55,
        "weigh": 55,
        "user_id": 970,
        "type": "interest",
        "content": "🎵音乐：听的风格很杂...\n🎮游戏：...\n📚书籍：..."
      },
      "tag": {
        "id": 28,
        "weigh": 28,
        "user_id": 970,
        "type": "tag",
        "content": "外向活力宝,人来疯,善解人意,自信"
      },
      "favorite": {
        "id": 54,
        "weigh": 54,
        "user_id": 970,
        "type": "favorite",
        "content": "理想型描述..."
      },
      "mbti": {
        "id": 27,
        "user_id": 970,
        "mbti_id": 5,
        "mbti": "INFJ",
        "mbti_data": {
          "id": 5,
          "name": "INFJ提倡者",
          "type": "INFJ",
          "content": "MBTI 描述...
          "definition": [
            { "id": 1, "content": "内倾型...", "type": "I" },
            { "id": 2, "content": "直觉型...", "type": "N" },
            { "id": 7, "content": "感觉型...", "type": "F" },
            { "id": 4, "content": "判断型...", "type": "J" }
          ]
        }
      },
      "questions_count": 1
    },
    "chat": {
      "id": 63,
      "user_id": 19,
      "contact_id": 970,
      "group": "19970",
      "read_status": 1,
      "status": 1,
      "user": {
        "id": 970,
        "nickname": "用户昵称",
        "avatar": "https://image.7dong.cc/...",
        "gender": 2
      }
    }
  }
}
```

**重要字段说明**：
- `user.pair`: 配对状态
- `user_pair_info`: 配对信息（生日、身高、地址、学历、工作等）
- `questions`: 问答列表，包含用户回答的内容和问题标题
- `userpairdata`: 扩展数据
  - `interest`: 兴趣标签（音乐、游戏、书籍等）
  - `tag`: 人格标签
  - `favorite`: 理想型描述
  - `mbti`: MBTI 人格，包含 `mbti_data` 详细数据和 `definition` 四维定义
  - `emotion`: 情感状态（可能为 null）
- `chat`: 聊天状态
- `lovestatus`: 恋爱状态

**重要说明**：此接口返回的数据已经包含用户完整信息，**不需要再调用其他接口**即可获取：
- 用户基本信息 (user)
- 配对信息 (user_pair_info)
- 问答列表 (questions)
- 扩展数据 (userpairdata)：包含情感状态、兴趣、标签、理想型、MBTI 等
- 聊天状态 (chat)

### 6. 聊天相关接口

#### 获取聊天列表
```
GET /miniapp/userchat/getuserchatlist?page=1
Headers: token (user_token)
```

#### 获取聊天记录
```
GET /miniapp/userchat/getuserchatrecord?receiver_id={user_id}&page=1
Headers: token (user_token)
```

#### 添加聊天（发送消息）
```
POST /miniapp/userchat/add
Headers: token (user_token)
Body:
{
 "message_type": "text",
 "content": "消息内容",
 "receiver_id": 接收者ID
}
```

**说明**：
- `message_type`: 聊天类型，可选值 `text`（文本）、`image`（图片）、`video`（视频）
- `content`: 消息内容
- `receiver_id`: 接收者用户ID（整数）

#### 聊天匹配
```
POST /miniapp/userchat/chat-matching
Headers: token (user_token)
Body:
{
 "content": "消息内容",
 "contact_id": "对方用户ID"
}
```

### 7. 帖子相关接口

#### 获取用户帖子
```
GET /miniapp/my/posting
Headers: token (user_token)
Body: { "user_id": 用户ID }
```
返回指定用户的帖子列表，包含帖子内容、点赞数、评论数、版块信息、话题信息等。
用于匹配分析时获取对方的发帖内容，了解对方的价值观和生活方式。

#### 发布帖子
```
POST /miniapp/posting/save
Headers: token (user_token)
Body:
{
 "type": "article",
 "content": "帖子内容",
 "topic_id": 版块ID,
 "images": "图片URL",
 "location": "位置",
 "subject_list": ["话题1", "话题2"]
}
```

#### 获取版块帖子
```
POST /miniapp/posting/topic
Headers: token (user_token)
Body: {"topic_id": 版块ID}
```

#### 喜欢帖子
```
POST /miniapp/attention/like
Headers: token (user_token)
Body: {"posting_id": 帖子ID}
```

### 8. 评论相关接口

#### 评论列表
```
POST /miniapp/comment/list
Headers: token (user_token)
Body: {"posting_id": 帖子ID}
```

#### 评论帖子
```
POST /miniapp/comment/save
Headers: token (user_token)
Body:
{
 "posting_id": 帖子ID,
 "content": "评论内容"
}
```

### 9. 问答相关接口

#### 获取问答列表
```
GET /miniapp/problem/list
Headers: token (user_token)
Parameters:
 - title: 搜索关键词（可选）
 - page: 页码（可选，默认1）
```

**返回数据结构：**
```json
{
 "code": 1,
 "data": {
   "total": 100,
   "per_page": 10,
   "current_page": 1,
   "last_page": 10,
   "data": [
     {
       "id": 1,
       "title": "问题标题"
     }
   ]
 }
}
```

#### 添加用户问答
```
POST /miniapp/questions/add
Headers: token (user_token)
Content-Type: multipart/form-data
Body:
 - problem_id: 问答ID
 - content: 回答内容
 - image: 图片（可选）
```

**说明：**
- 用于完善用户的问答信息
- 每个用户可以回答多个问题
- 建议至少回答 3-5 个问题以提高匹配质量

### 10. 用户相关接口

#### 获取当前用户信息
```
POST /miniapp/user/info
Headers: token (user_token)
```

**返回数据结构：**
```json
{
 "code": 1,
 "data": {
 "id": 用户ID,
 "nickname": "昵称",
 "avatar": "头像URL",
 "gender": 1,
 "bio": "个性签名",
 "user_info": {
 "birthday": "1989-09-07",
 "height": "170",
 "address": "广东省/xxx",
 "education": "学历",
 "work": "职业",
 "constellation": "星座,
 "employment_company": "公司"
 }
 }
}
```

#### 完善个人扩展信息
```
POST /miniapp/user/editextend
Headers: token (user_token)
Content-Type: application/json
Body:
{
 "is_graduate": 1,        // 是否毕业：0=在读，1=已毕业
 "grade": "2013级",       // 年级
 "major": "计算机科学",    // 专业
 "college": "信息学院",    // 学院
 "school": "XX大学",       // 学校
 "edu": "本科",           // 学历
 "marriage": "未婚",       // 婚姻状况
 "income": 200000,        // 年收入
 "industry": "互联网",     // 行业
 "lng": 112.7463,         // 经度
 "lat": 20.8045,          // 纬度
 "address": "详细地址",     // 详细地址
 "county": "松山湖",       // 区县
 "city": "东莞市",         // 城市
 "province": "广东省"      // 省份
}
```

**说明：**
- 此接口用于完善用户的扩展个人信息
- 教育相关：school, college, major, grade, edu, is_graduate
- 工作相关：industry, income
- 地址相关：province, city, county, address, lng, lat
- 个人情况：marriage

#### 获取推荐偏好
```
GET /miniapp/rd/getrddata
Headers: token (user_token)
```

**返回数据结构：**
```json
{
 "code": 1,
 "data": {
 "address": "省/市",
 "education": "学历期望",
 "min_age": 18,
 "max_age": 60,
 "min_height": 100,
 "max_height": 220
 }
}
```

#### 设置推荐偏好
```
POST /miniapp/rd/add
Headers: token (user_token)
Body:
{
 "address": "广东省/东莞市",
 "education": "本科",
 "min_age": 18,
 "max_age": 35,
 "min_height": 150,
 "max_height": 180,
 "rcert_status": 0,
 "rmwil_status": 0
}
```