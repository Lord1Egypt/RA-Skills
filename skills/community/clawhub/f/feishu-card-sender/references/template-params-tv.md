# template: `tv-custom`

模板文件：`assets/templates/tv-custom.json`

## 必填参数

- title
- overview
- rating
- first_air_date
- status
- seasons_episodes（示例：`3 季 / 24 集`）
- episode_runtime（示例：`45 分钟`）
- genres
- country
- creator
- cast（Markdown 多行字符串）
- detail_url（TMDB 详情页）
- tmdb_id（TMDB 条目 ID，用于“立即订阅”回调）
- media_type（`tv`，可不传，规则默认补齐）
- subscribe_disabled（`true|false`，可选，控制“立即订阅”按钮禁用）
- subscribe_button_text（可选，默认“立即订阅”）
- poster_img_key（或通过 `--poster-url/--poster-file` 自动注入）

## 可选参数

- tagline（为空时自动不渲染该区块）

## 发送示例

```bash
python3 scripts/send_feishu_card.py \
  --template tv-custom \
  --receive-id ou_xxx \
  --receive-id-type open_id \
  --account-id current \
  --poster-url 'https://image.tmdb.org/t/p/original/xxx.jpg' \
  --var title='黑镜' \
  --var overview='...' \
  --var rating='8.4 / 10' \
  --var first_air_date='2011-12-04' \
  --var status='Returning Series' \
  --var seasons_episodes='6 季 / 27 集' \
  --var episode_runtime='60 分钟' \
  --var genres='剧情 / 科幻 / 惊悚' \
  --var country='英国' \
  --var creator='Charlie Brooker' \
  --var cast='• **演员A** 饰 角色A' \
  --var detail_url='https://www.themoviedb.org/tv/42009'
```
