# Anime Character Loader

通过AniList API查询二次元角色信息，自动生成OpenClaw标准的SOUL.md人设文件。

## 功能

- 🔍 支持英文/日文/中文角色名查询
- 📝 自动生成SOUL.md格式的人设文件
- 🌐 使用AniList GraphQL API（无需API Key）
- 🎯 包含角色性格、说话方式、边界等章节

## 安装

```bash
# 进入skill目录
cd skills/anime-character-loader

# 安装依赖
pip install requests
```

## 使用方法

### 基本用法

```bash
python load_character.py "角色名"
```

### 示例

```bash
# 使用英文/日文名
python load_character.py "Kasumigaoka Utaha"
python load_character.py "Misaka Mikoto"

# 使用中文名（已支持映射）
python load_character.py "霞之丘诗羽"
python load_character.py "加藤惠"
python load_character.py "御坂美琴"

# 仅显示角色信息，不生成文件
python load_character.py "Sakurajima Mai" --info

# 指定输出目录
python load_character.py "Makise Kurisu" -o ./characters/
```

## 支持的中文角色名

| 中文名 | 日文名 | 英文名 | 出处 |
|--------|--------|--------|------|
| 霞之丘诗羽 | 霞ヶ丘詩羽 | Utaha Kasumigaoka | 路人女主的养成方法 |
| 加藤惠 | 加藤恵 | Megumi Katou | 路人女主的养成方法 |
| 御坂美琴 | 御坂美琴 | Mikoto Misaka | 某科学的超电磁炮 |

更多角色可以在 `load_character.py` 中的 `NAME_MAPPING` 添加映射。

## 生成的SOUL.md结构

```markdown
# 角色名

**Source:** 出处作品
**Japanese Name:** 日文名
**Also Known As:** 别名

## Identity
角色身份定义

## Background
角色背景故事

## Personality
性格特征列表

## Speaking Style
说话方式和特点

## Boundaries
角色扮演边界和规则
```

## 配置说明

无需API Key，AniList API完全免费。

如需添加更多中文名映射，编辑 `load_character.py`：

```python
NAME_MAPPING = {
    "中文名": "English Name",
    # ... 添加更多
}
```

## 技术细节

- **Python**: 3.10+
- **依赖**: requests
- **API**: AniList GraphQL (https://graphql.anilist.co)
- **数据**: 角色信息、描述、出处作品、别名

## 测试报告

查看 [TEST_REPORT.md](TEST_REPORT.md) 了解详细测试结果。

## 许可

MIT License
