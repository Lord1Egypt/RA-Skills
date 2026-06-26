# Publishing Examples

Read this file when you need a concrete invocation pattern.

## Publish a single image from a URL

```bash
python3 scripts/publish_instagram.py \
  --type IMAGE \
  --url "https://example.com/image.jpg" \
  --caption "Hello World!"
```

## Publish a reel from a local file

```bash
python3 scripts/publish_instagram.py \
  --type REELS \
  --path "/path/to/video.mp4" \
  --caption "Check this out!" \
  --thumb-offset 1000
```

## Publish a mixed carousel

```bash
python3 scripts/publish_instagram.py \
  --type CAROUSEL \
  --items "/path/to/img1.jpg" "https://example.com/vid2.mp4" \
  --caption "My Carousel"
```

## Check status

```bash
python3 scripts/publish_instagram.py \
  --check-id "v_pub_file~123"
```

## Fetch recent direct messages

```bash
python3 scripts/receive_messages.py \
  --limit 25
```

## Send a direct message

```bash
python3 scripts/send_message.py \
  --conversation-id "CONVERSATION_ID" \
  --message "Thanks for reaching out!"
```

Instagram direct messaging is subject to Meta platform policy and messaging-window
limits. If the API returns an error such as `(#10) This message is sent outside
of allowed window`, report the real response instead of retrying indefinitely.
