# RPA Tasks Guide

Complete guide to GeeLark's built-in RPA (Robotic Process Automation) tasks for 9 major platforms.

---

## Overview

GeeLark provides pre-built RPA tasks for automating operations on:

- **TikTok** - Login, follow, like, comment, edit, delete
- **Instagram** - Login, publish reels, warmup
- **Facebook** - Login, publish, auto-comment, active account
- **YouTube** - Publish short, publish video, active account
- **Reddit** - Publish image/video, warmup
- **Threads** - Publish image/video
- **Pinterest** - Publish image/video
- **X (Twitter)** - Publish post
- **Google** - Login, app download, app browse

---

## Common Parameters

All RPA tasks use these common parameters:

```json
{
  "name": "task_name",
  "remark": "task_remark",
  "scheduleAt": 1741846843,  // Unix timestamp (required)
  "id": "phoneId"  // Cloud phone ID (required)
}
```

**Note**: `scheduleAt` is required for all RPA tasks. Use `Math.floor(Date.now() / 1000) + delay` to schedule future tasks.

---

## TikTok

### Login

```python
client.rpa_task("tiktokLogin", {
    "id": phone_id,
    "account": "test@gmail.com",
    "password": "123456",
    "scheduleAt": int(time.time()) + 60,
    "name": "TikTok Login"
})
```

### Random Follow

```python
client.rpa_task("tiktokRandomFollow", {
    "id": phone_id,
    "followProbability": 30,  // 0-100, probability of following
    "scheduleAt": int(time.time()) + 60,
    "name": "Random Follow"
})
```

### Random Like

```python
client.rpa_task("tiktokRandomStar", {
    "id": phone_id,
    "scheduleAt": int(time.time()) + 60,
    "name": "Random Like"
})
```

### Random Comment

```python
client.rpa_task("tiktokRandomComment", {
    "id": phone_id,
    "useAi": 1,  // 1 = AI comment, 2 = manual comment
    "comment": "Nice video!",  // Required if useAi=2
    "scheduleAt": int(time.time()) + 60,
    "name": "Random Comment"
})
```

### Edit Video

```python
client.rpa_task("tiktokEdit", {
    "id": phone_id,
    "scheduleAt": int(time.time()) + 60,
    "name": "Edit Video"
})
```

### Delete Video

```python
client.rpa_task("tiktokDel", {
    "id": phone_id,
    "scheduleAt": int(time.time()) + 60,
    "name": "Delete Video"
})
```

### Hide Video

```python
client.rpa_task("tiktokHide", {
    "id": phone_id,
    "scheduleAt": int(time.time()) + 60,
    "name": "Hide Video"
})
```

---

## Instagram

### Login

```python
client.rpa_task("instagramLogin", {
    "id": phone_id,
    "account": "test@gmail.com",
    "password": "123456",
    "scheduleAt": int(time.time()) + 60,
    "name": "Instagram Login"
})
```

### Publish Reels (Video)

```python
client.rpa_task("instagramPubReels", {
    "id": phone_id,
    "description": "Amazing reels!",
    "video": ["/path/to/video.mp4"],  // Array of file paths
    "scheduleAt": int(time.time()) + 60,
    "name": "Publish Reels"
})
```

### Publish Reels (Images)

```python
client.rpa_task("instagramPubReelsImages", {
    "id": phone_id,
    "Image": ["/path/to/image1.jpg", "/path/to/image2.jpg"],  // Note: Capital 'I'
    "scheduleAt": int(time.time()) + 60,
    "name": "Publish Reels Images"
})
```

**Note**: Field name is `Image` (not `images`) for `instagramPubReelsImages`

### Edit Post

```python
client.rpa_task("instagramEdit", {
    "id": phone_id,
    "scheduleAt": int(time.time()) + 60,
    "name": "Edit Post"
})
```

### Account Warmup

```python
client.rpa_task("instagramWarmup", {
    "id": phone_id,
    "scheduleAt": int(time.time()) + 60,
    "name": "Account Warmup"
})
```

---

## Facebook

### Login

```python
client.rpa_task("faceBookLogin", {
    "id": phone_id,
    "Email": "test@gmail.com",  // Note: 'Email' not 'account'
    "Password": "123456",
    "scheduleAt": int(time.time()) + 60,
    "name": "Facebook Login"
})
```

**Note**: Field name is `Email` (not `account`) for `faceBookLogin`

### Publish Video

```python
client.rpa_task("faceBookPublish", {
    "id": phone_id,
    "title": "My Video",
    "video": ["/path/to/video.mp4"],  // Array of file paths
    "scheduleAt": int(time.time()) + 60,
    "name": "Publish Video"
})
```

### Publish Reels

```python
client.rpa_task("faceBookPubReels", {
    "id": phone_id,
    "title": "My Reels",
    "video": "/path/to/video.mp4",  // String, not array
    "scheduleAt": int(time.time()) + 60,
    "name": "Publish Reels"
})
```

**Note**: Facebook Reels uses `video` as a string, not an array

### Auto Comment

```python
client.rpa_task("faceBookAutoComment", {
    "id": phone_id,
    "PostAddress": "https://facebook.com/post/123",
    "Comment": "Great post!",
    "Keyword": "amazing",
    "scheduleAt": int(time.time()) + 60,
    "name": "Auto Comment"
})
```

### Active Account

```python
client.rpa_task("faceBookActiveAccount", {
    "id": phone_id,
    "BrowsePostsNum": 10,
    "Keyword": "technology",
    "scheduleAt": int(time.time()) + 60,
    "name": "Active Account"
})
```

---

## YouTube

### Publish Short

```python
client.rpa_task("youtubePubShort", {
    "id": phone_id,
    "title": "My Short",
    "video": "/path/to/video.mp4",  // String, not array
    "sameStyleVoice": True,
    "originalVoice": False,
    "scheduleAt": int(time.time()) + 60,
    "name": "Publish Short"
})
```

**Note**: YouTube uses `video` as a string, not an array

### Publish Video

```python
client.rpa_task("youtubePubVideo", {
    "id": phone_id,
    "title": "My Video",
    "video": "/path/to/video.mp4",
    "description": "Video description here",
    "scheduleAt": int(time.time()) + 60,
    "name": "Publish Video"
})
```

### Active Account

```python
client.rpa_task("youTubeActiveAccount", {
    "id": phone_id,
    "BrowseVideoNum": 10,
    "Keyword": "music",
    "scheduleAt": int(time.time()) + 60,
    "name": "Active Account"
})
```

---

## Reddit

### Publish Image

```python
client.rpa_task("redditImage", {
    "id": phone_id,
    "title": "My Image Post",
    "images": ["/path/to/image1.jpg", "/path/to/image2.jpg"],  // Array
    "community": "r/pics",
    "scheduleAt": int(time.time()) + 60,
    "name": "Publish Image"
})
```

### Publish Video

```python
client.rpa_task("redditVideo", {
    "id": phone_id,
    "title": "My Video Post",
    "video": ["/path/to/video.mp4"],  // Array
    "community": "r/videos",
    "scheduleAt": int(time.time()) + 60,
    "name": "Publish Video"
})
```

### Account Warmup

```python
client.rpa_task("redditWarmup", {
    "id": phone_id,
    "scheduleAt": int(time.time()) + 60,
    "name": "Account Warmup"
})
```

---

## Threads

### Publish Image

```python
client.rpa_task("threadsImage", {
    "id": phone_id,
    "title": "My Thread",
    "images": ["/path/to/image1.jpg", "/path/to/image2.jpg"],  // Array
    "scheduleAt": int(time.time()) + 60,
    "name": "Publish Image"
})
```

### Publish Video

```python
client.rpa_task("threadsVideo", {
    "id": phone_id,
    "title": "My Thread",
    "video": ["/path/to/video.mp4"],  // Array
    "scheduleAt": int(time.time()) + 60,
    "name": "Publish Video"
})
```

---

## Pinterest

### Publish Image

```python
client.rpa_task("pinterestImage", {
    "id": phone_id,
    "title": "My Pin",
    "description": "Pin description",
    "images": ["/path/to/image1.jpg", "/path/to/image2.jpg"],  // Array
    "scheduleAt": int(time.time()) + 60,
    "name": "Publish Image"
})
```

### Publish Video

```python
client.rpa_task("pinterestVideo", {
    "id": phone_id,
    "title": "My Pin",
    "description": "Pin description",
    "video": ["/path/to/video.mp4"],  // Array
    "scheduleAt": int(time.time()) + 60,
    "name": "Publish Video"
})
```

---

## X (Twitter)

### Publish Post

```python
client.rpa_task("xPublish", {
    "id": phone_id,
    "description": "My tweet",
    "video": ["/path/to/video.mp4"],  // Array
    "scheduleAt": int(time.time()) + 60,
    "name": "Publish Tweet"
})
```

---

## Google

### Login

```python
client.rpa_task("googleLogin", {
    "id": phone_id,
    "Email": "test@gmail.com",
    "Password": "123456",
    "scheduleAt": int(time.time()) + 60,
    "name": "Google Login"
})
```

### App Download

```python
client.rpa_task("googleAppDownload", {
    "id": phone_id,
    "appName": "WhatsApp",
    "scheduleAt": int(time.time()) + 60,
    "name": "Download App"
})
```

### App Browse

```python
client.rpa_task("googleAppBrowser", {
    "id": phone_id,
    "appName": "Instagram",
    "scheduleAt": int(time.time()) + 60,
    "name": "Browse App"
})
```

---

## Shein

### Login

```python
client.rpa_task("sheinLogin", {
    "id": phone_id,
    "Email": "test@gmail.com",
    "Password": "123456",
    "scheduleAt": int(time.time()) + 60,
    "name": "Shein Login"
})
```

---

## Task Management

### Query Task Status

```python
response = client.call("/open/v1/task/query", {
    "ids": [task_id]
})

status = response['data']['items'][0]['status']
print(f"Task status: {status}")
```

### Get Task Details

```python
response = client.call("/open/v1/task/detail", {
    "ID": task_id  # Note: uppercase 'ID'
})

details = response['data']
print(f"Task details: {details}")
```

### Cancel Task

```python
response = client.call("/open/v1/task/cancel", {
    "ids": [task_id]
})

if response['code'] == 0:
    print("✅ Task cancelled")
```

### Get Task History

```python
response = client.call("/open/v1/task/historyRecords", {
    "page": 1,
    "pageSize": 50
})

tasks = response['data']['items']
for task in tasks:
    print(f"Task: {task['name']}, Status: {task['status']}")
```

---

## Best Practices

### 1. Schedule Tasks in the Future

```python
# Schedule task 60 seconds from now
schedule_at = int(time.time()) + 60

client.rpa_task("tiktokLogin", {
    "id": phone_id,
    "account": "test@gmail.com",
    "password": "123456",
    "scheduleAt": schedule_at
})
```

### 2. Use Meaningful Task Names

```python
client.rpa_task("tiktokRandomFollow", {
    "id": phone_id,
    "followProbability": 30,
    "scheduleAt": schedule_at,
    "name": "Daily Follow Routine - Account 1",  # Meaningful name
    "remark": "Follow 30% probability, niche: tech"  # Detailed remark
})
```

### 3. Check Task Status After Scheduling

```python
response = client.rpa_task("tiktokLogin", {...})

if response['code'] == 0:
    task_id = response['data']['taskId']
    print(f"✅ Task created: {task_id}")

    # Poll task status
    import time
    while True:
        status = client.call("/open/v1/task/query", {"ids": [task_id]})
        task_status = status['data']['items'][0]['status']

        if task_status == 'success':
            print("✅ Task completed successfully")
            break
        elif task_status == 'failed':
            print("❌ Task failed")
            break

        time.sleep(10)  # Check every 10 seconds
```

### 4. Handle Errors Gracefully

```python
response = client.rpa_task("tiktokLogin", {...})

if response['code'] != 0:
    error_msg = response.get('msg', 'Unknown error')
    print(f"❌ Task creation failed: {error_msg}")

    # Check fail details
    if response.get('data', {}).get('failAmount', 0) > 0:
        for fail in response['data']['failDetails']:
            print(f"   Error: {fail.get('msg')}")
```

---

## Video Parameter Format Summary

| Platform | Video Format | Example |
|----------|-------------|---------|
| **TikTok** | Array | `"video": ["/path/to/video.mp4"]` |
| **Instagram** | Array | `"video": ["/path/to/video.mp4"]` |
| **Instagram Reels Images** | Array (Capital 'I') | `"Image": ["/path/to/image.jpg"]` |
| **Facebook** | Array | `"video": ["/path/to/video.mp4"]` |
| **Facebook Reels** | String | `"video": "/path/to/video.mp4"` |
| **YouTube** | String | `"video": "/path/to/video.mp4"` |
| **Reddit** | Array | `"video": ["/path/to/video.mp4"]` |
| **Threads** | Array | `"video": ["/path/to/video.mp4"]` |
| **Pinterest** | Array | `"video": ["/path/to/video.mp4"]` |
| **X** | Array | `"video": ["/path/to/video.mp4"]` |

**Key Differences**:
- YouTube: `video` is a **string**
- Facebook Reels: `video` is a **string**
- Instagram Images: Field name is `Image` (capital 'I')
- All others: `video` or `images` is an **array**

---

## Field Name Summary

| Platform | Login Account Field | Notes |
|----------|-------------------|-------|
| **TikTok** | `account` | - |
| **Instagram** | `account` | - |
| **Facebook** | `Email` | Capital 'E' |
| **Google** | `Email` | Capital 'E' |
| **Shein** | `Email` | Capital 'E' |

---

## Last Updated

2026-04-10

**Related Documents**:
- [API Reference](api_reference.md) - Complete endpoint list
- [Best Practices](best_practices.md) - Safety and performance tips