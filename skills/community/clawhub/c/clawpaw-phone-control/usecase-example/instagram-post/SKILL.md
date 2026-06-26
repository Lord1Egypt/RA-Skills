---
name: instagram-post
description: Create and publish an Instagram post with a photo and caption. Use when user says "post to Instagram", "share on IG", "upload a photo to Instagram", etc.
disable-model-invocation: true
---

# Instagram Post

Create and publish an Instagram post. Instagram's API is extremely limited for personal accounts — posting with full features (filters, tagging, location) can only be done via the app.

Use `snapshot` throughout. Avoid `screenshot` unless snapshot returns no useful elements.

## Package

`com.instagram.android`

## Step 1 — Launch Instagram

```
shell → monkey -p com.instagram.android -c android.intent.category.LAUNCHER 1
```

`snapshot` — confirm Instagram is open and the user is logged in. If a login page appears (elements with desc "登录" or "Log in"), inform the user they need to log in first and stop.

## Step 2 — Open create flow

Instagram's bottom tab bar has a "+" button for creating content.

1. `snapshot` — find the create button. Look for:
   - desc containing "Create" or "New post" or "创建"
   - Or the center icon in the bottom navigation bar (usually the 3rd of 5 tabs)
2. `tap` the create button
3. `snapshot` — should show the photo picker / gallery view

## Step 3 — Select a photo

The gallery picker shows recent photos from the device.

1. `snapshot` — look for the photo grid. Photos are usually in a grid of `ImageView` elements
2. **If user specified a photo:** scroll to find it, or use the gallery/album selector
3. **If no specific photo:** tap the first (most recent) photo in the grid
4. `snapshot` — confirm a photo is selected (it should appear in the preview area at the top)
5. Look for "Next" or "下一步" button → `tap`

## Step 4 — Edit (optional)

The filter/edit screen appears:

1. `snapshot` — look for filter options and the "Next" / "下一步" button
2. Skip filters unless the user requested one
3. `tap` "Next" / "下一步" to proceed to the caption screen

## Step 5 — Write caption

1. `snapshot` — find the caption input field. Look for:
   - desc or text containing "Write a caption" or "添加说明"
   - An `EditText` element near the top of the screen
2. `tap` the caption field
3. `type_text` with the caption from `$ARGUMENTS` or as specified by the user
4. If the user wants hashtags, append them to the caption

## Step 6 — Publish

1. `snapshot` — find the "Share" / "分享" button (usually top-right)
2. **Confirm with the user** before tapping: "Ready to post with caption: '...'. Shall I publish?"
3. After user confirms, `tap` the Share button
4. `snapshot` — verify the post was published (should return to feed or profile)

## Important Notes

1. **Always confirm before publishing** — this is an irreversible action visible to followers
2. **Instagram uses a mix of native and WebView elements** — some screens may require `screenshot` as fallback if snapshot returns minimal elements
3. **Stories and Reels** have different flows — this skill covers regular feed posts only
4. **Multiple photos (carousel):** After selecting the first photo, look for a "Select multiple" / "多选" button to add more photos before proceeding
5. **Location tagging:** On the caption screen, look for "Add location" / "添加地点" if the user wants to tag a location
6. **Tagging people:** Look for "Tag people" / "标记用户" option on the caption screen
7. **The create button position varies by Instagram version** — if not found in bottom nav, try the "+" icon in the top-right of the home screen
