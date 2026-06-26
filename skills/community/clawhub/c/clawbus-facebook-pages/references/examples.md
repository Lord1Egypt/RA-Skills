# Examples

Read this file when you need a concrete invocation pattern.

## Connect Facebook Pages

```bash
python3 scripts/facebook_pages.py \
  connect
```

## List connected accounts

```bash
python3 scripts/facebook_pages.py \
  list-connections
```

## List available Pages

```bash
python3 scripts/facebook_pages.py \
  list-accounts
```

## Publish a Page post

```bash
python3 scripts/facebook_pages.py \
  publish-post \
  --page-id "PAGE_ID" \
  --message "Hello from the Pages API!" \
  --link "https://www.mybrandmetrics.com"
```

## Publish a Page photo

```bash
python3 scripts/facebook_pages.py \
  publish-photo \
  --page-id "PAGE_ID" \
  --url "https://example.com/image.jpg" \
  --caption "Photo from the Pages API"
```

## Publish a Page video

```bash
python3 scripts/facebook_pages.py \
  publish-video \
  --page-id "PAGE_ID" \
  --url "https://example.com/video.mp4" \
  --caption "Video from the Pages API"
```

## Read a Page feed

```bash
python3 scripts/facebook_pages.py \
  feed \
  --page-id "PAGE_ID" \
  --limit 25
```

## Read comments

```bash
python3 scripts/facebook_pages.py \
  comments \
  --page-id "PAGE_ID" \
  --object-id "POST_ID" \
  --limit 25
```

## Create a comment

```bash
python3 scripts/facebook_pages.py \
  comment-create \
  --page-id "PAGE_ID" \
  --object-id "POST_ID" \
  --message "Thanks for your comment!"
```

## Update or hide a comment

```bash
python3 scripts/facebook_pages.py \
  comment-update \
  --page-id "PAGE_ID" \
  --comment-id "COMMENT_ID" \
  --hide
```

## Delete a comment

```bash
python3 scripts/facebook_pages.py \
  comment-delete \
  --page-id "PAGE_ID" \
  --comment-id "COMMENT_ID"
```

## Page insights

```bash
python3 scripts/facebook_pages.py \
  insights \
  --page-id "PAGE_ID" \
  --metrics "page_impressions,page_fans"
```

## Post insights

```bash
python3 scripts/facebook_pages.py \
  post-insights \
  --post-id "POST_ID" \
  --metrics "post_impressions,post_impressions_unique"
```
