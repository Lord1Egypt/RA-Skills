在AddSession接口中，有一个可选字段profiles，其作用是定义需要特别关注或更新的画像信息列表。如不定义，系统会自行判断更新哪些画像。如果手动指定，则只会在指定的画像范围内进行更新。
| **参数名** | **类型** | **是否必须** | **描述** |
| --- | --- | --- | --- |
| profiles | Array of Object | 否 | 需要特别关注或更新的画像信息列表。系统会尝试将处理后的事件与这些画像关联。 |
| * profile_type | String | 是 | 画像类型名称，必须是记忆库中已定义的画像类型。 |
| * profile_scope | Array of Object | 是 | 具体的画像实例列表。每个对象包含用于唯一标识和定义该画像实例的属性，例如: {"id": 1, "knowledge_point_name": "taco"} |

**什么时候需要指定画像更新范围呢？**
在使用模板画像时，画像记忆默认是 user_id 维度的，如果不为画像定义“自定义主键字段（"IsPrimaryKey": true）”， 那么每个画像规则会为每个 user_id 维护一条记录。模板里默认用户画像（user_profile）就是一种典型的 user_id 维度的画像记忆。

**设置了自定义主键的画像记忆**
在无主键画像记忆的基础上，我们还支持了给定主键的画像记忆。 比如我们想关注用户对于某一个电影的记忆，可以定义一个主键字段 movie_name， 这时候实际上的存储主键为：['movie_name', 'user_id'] ，我们会为每个用户下的每个movie_name 维护一份状态， 检索时可以基于`画像规则名称+电影名`来进行检索。
配置如下：
| 事件规则 | 画像规则 |
| --- | --- |
| ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/c9cc9c7f5de641cd8043bc1fb50b58c6~tplv-goo7wpa0wc-image.image) <br>  | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/f07b09ba1857488aaec5d1617b7e8641~tplv-goo7wpa0wc-image.image) |
**定义自定义主键抽取的范围**
上面的配置定义，实现的效果是：让大模型来抽取 movie_name，但是有些更定制化的情况，我们希望大模型抽取的信息是能够关联到业务数据的，比如在影评分析的场景，我们希望影评的记忆可以关联到我们内部电影库的某一条唯一的记录（或者在教学场景， 希望关联到某个知识点集合中的一条记录）， 这种时候如果这个主键是让大模型先抽取，再去关联业务数据，很多时候会产生偏差（比如知识点的粒度不一致）。
我们的做法是允许用户在抽取记忆时可以提供画像的主键范围，在上传事件时为每一段对话指定画像范围。
在调用 AddSession 接口时可以提供 profiles 字段来约束大模型抽取内容时，只关注输入的这些画像。例如：
```Python
payload = {
    "collection_name": "collection_name",
    "session_id": "xxx",
    "messages": [
    ...
    ],
    "metadata": {
    ...
    },
    "profiles": [
        {
          "profile_type": "movie_preferences",
          "profile_scope": [
            { 
              "movie_id": 201, # 业务数据库中的电影id
              "movie_name": "碟中谍 6：全面瓦解",
              "movie_alias": ["不可能的任务：全面瓦解", "职业特工队：叛逆之谜", "Mission: Impossible – Fallout"]
            }，
            { 
              "movie_id": 202, # 业务数据库中的电影id
              "movie_name": "夺宝奇兵 5：命运转盘",
              "movie_alias": ["印第安纳琼斯：命运轮盘", "Indiana Jones and the Dial of Destiny"]
            }
          ]
        }
    ]
}
```

在 profile_scope 中，需要提供大模型认识的有语义含义的字段信息，给大模型提供更多信息来做“选择题”，而非“填空题”，类似于给大模型 few shot。
上面👆的例子中，如果只给大模型提供 movie_id 这一列，那么在写入一段新的对话，很可能对于讲同一个电影的对话，抽取出了不同的两个画像实体。
