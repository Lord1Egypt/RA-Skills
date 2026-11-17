---
name: "meta-ads-report"
description: "Kéo báo cáo chỉ số Meta Ads (Facebook/Instagram) qua Graph API. READ-ONLY: insights, campaign, account, kiểm tra hạn token."
---

# Meta Ads Report (READ-ONLY)

Kéo chỉ số báo cáo quảng cáo Meta qua **Graph API chính thức** bằng HTTP (curl) — không cần SDK.

> ⚠️ **Tuyệt đối READ-ONLY.** Skill này CHỈ đọc dữ liệu (insights + danh sách campaign/account). KHÔNG có bất kỳ lệnh tạo/sửa/tắt/xóa ads nào. Không bao giờ gọi POST/DELETE tới Graph API.

## 1. Cấu hình (environment variables)

| Biến | Bắt buộc | Mô tả |
|------|----------|-------|
| `META_ACCESS_TOKEN` | ✅ | Meta access token (User token hoặc System User token), quyền `ads_read` |
| `META_AD_ACCOUNT_ID` | ✅ | Ad account ID dạng số (không có prefix `act_`), ví dụ `123456789` |

**Lưu ý bảo mật:**
- Token đọc từ **environment variable**, KHÔNG hardcode trong file/skill.
- Đặt token trong config `env` của gateway (instance OpenClaw của bạn), không commit vào script.
- **KHÔNG bao giờ nhét token trực tiếp vào URL bằng dấu ngoặc kép** → shell cắt chuỗi → lỗi 4xx GIẢ (trông như token hỏng nhưng thật ra URL bị cắt). Luôn dùng `curl -G --data-urlencode "access_token=$META_ACCESS_TOKEN"`.

## 2. Lấy token (tài khoản cá nhân)

1. Vào `developers.facebook.com/tools/explorer`
2. Chọn app loại "Business" (tạo mới nếu chưa có)
3. Thêm quyền `ads_read` (+ `ads_management` nếu cần)
4. **Generate Access Token** → đăng nhập → cho phép
5. Copy token test (ngắn hạn ~2h)

**Chuyển sang long-lived (~60 ngày):**
```bash
curl -G "https://graph.facebook.com/v21.0/oauth/access_token" \
  --data-urlencode "grant_type=fb_exchange_token" \
  --data-urlencode "client_id={APP_ID}" \
  --data-urlencode "client_secret={APP_SECRET}" \
  --data-urlencode "fb_exchange_token={SHORT_LIVED_TOKEN}"
```

> Token cá nhân long-lived hết hạn sau ~60 ngày → phải đăng nhập lại lấy token mới (không tự gia hạn hoàn toàn được vì cần phiên đăng nhập). Nên tự kiểm tra hạn bằng `debug_token` và cảnh báo trước <14 ngày.

## 3. Cách dùng — các lệnh đọc (CHỈ GET)

**1. Kiểm tra token & hạn dùng**
```bash
curl -s -G "https://graph.facebook.com/v21.0/debug_token" \
  --data-urlencode "input_token=$META_ACCESS_TOKEN" \
  --data-urlencode "access_token=$META_ACCESS_TOKEN"
```
Đọc `data.is_valid` và `data.expires_at` (epoch giây). Nếu hết hạn <14 ngày → cảnh báo người dùng đăng nhập lại.

**2. Thông tin ad account**
```bash
curl -s -G "https://graph.facebook.com/v21.0/act_$META_AD_ACCOUNT_ID" \
  --data-urlencode "fields=name,account_status,currency,timezone_name,amount_spent,balance,spend_cap" \
  --data-urlencode "access_token=$META_ACCESS_TOKEN"
```

**3. Danh sách campaign**
```bash
curl -s -G "https://graph.facebook.com/v21.0/act_$META_AD_ACCOUNT_ID/campaigns" \
  --data-urlencode "fields=id,name,status,objective,daily_budget,lifetime_budget" \
  --data-urlencode "limit=100" \
  --data-urlencode "access_token=$META_ACCESS_TOKEN"
```

**4. Báo cáo tổng (account-level) theo preset**
```bash
curl -s -G "https://graph.facebook.com/v21.0/act_$META_AD_ACCOUNT_ID/insights" \
  --data-urlencode "fields=spend,impressions,clicks,reach,cpc,cpm,ctr,actions,action_values" \
  --data-urlencode "date_preset=last_7d" \
  --data-urlencode "access_token=$META_ACCESS_TOKEN"
```

**5. Báo cáo theo khoảng ngày tùy chỉnh**
```bash
curl -s -G "https://graph.facebook.com/v21.0/act_$META_AD_ACCOUNT_ID/insights" \
  --data-urlencode "fields=spend,impressions,clicks,reach,actions,action_values" \
  --data-urlencode 'time_range={"since":"2026-01-01","until":"2026-01-31"}' \
  --data-urlencode "access_token=$META_ACCESS_TOKEN"
```

**6. Báo cáo từng CAMPAIGN (kèm objective)**
```bash
curl -s -G "https://graph.facebook.com/v21.0/act_$META_AD_ACCOUNT_ID/insights" \
  --data-urlencode "fields=campaign_name,campaign_id,objective,spend,impressions,clicks,reach,frequency,cpc,cpm,ctr,actions,action_values" \
  --data-urlencode "level=campaign" \
  --data-urlencode "date_preset=last_7d" \
  --data-urlencode "access_token=$META_ACCESS_TOKEN"
```

**7. Báo cáo từng ngày (time_increment=1)**
```bash
curl -s -G "https://graph.facebook.com/v21.0/act_$META_AD_ACCOUNT_ID/insights" \
  --data-urlencode "fields=spend,impressions,clicks,ctr,actions,action_values" \
  --data-urlencode "time_increment=1" \
  --data-urlencode "date_preset=last_7d" \
  --data-urlencode "access_token=$META_ACCESS_TOKEN"
```

**8. Breakdown (tuổi / giới tính / vị trí)**
```bash
curl -s -G "https://graph.facebook.com/v21.0/act_$META_AD_ACCOUNT_ID/insights" \
  --data-urlencode "fields=spend,impressions,clicks,cpc" \
  --data-urlencode "breakdowns=age,gender" \
  --data-urlencode "date_preset=last_7d" \
  --data-urlencode "access_token=$META_ACCESS_TOKEN"
```

**9. Liệt kê các ad account user sở hữu (để biết ID nào kéo được)**
```bash
curl -s -G "https://graph.facebook.com/v21.0/me/adaccounts" \
  --data-urlencode "fields=name,account_id,account_status,currency" \
  --data-urlencode "limit=200" \
  --data-urlencode "access_token=$META_ACCESS_TOKEN"
```

## 4. Chỉ số thường dùng

`spend` (chi phí) · `impressions` · `clicks` · `reach` · `frequency` · `cpc` · `cpm` · `ctr` · `actions` (hành động/chuyển đổi) · `action_values` (giá trị chuyển đổi → tính ROAS).

**ROAS** = `action_values` / `spend`.

**Ánh xạ objective → action_type kết quả chính (KHÔNG lấy bừa `lead` cho mọi camp):**
- `OUTCOME_ENGAGEMENT` / MESSAGES → `onsite_conversion.messaging_conversation_started_7d` = "tin nhắn mở chat". (KHÔNG dùng `lead`/`onsite_web_lead`.)
- `OUTCOME_SALES` / PURCHASES → `omni_purchase` = "lượt mua" (khớp cột Ads Manager; tránh `purchase`/`onsite_conversion.purchase` hay trống).
- `OUTCOME_LEADS` / LEAD_GENERATION → `lead` hoặc `onsite_conversion.lead` = "lead điền form".
- `OUTCOME_TRAFFIC` → `link_click` / `outbound_click` = "lượt click".
- Quảng cáo livestream (tên camp chứa `LIVE`) → tương tác chính là `post_comment` (lượt bình luận).

## 5. Xử lý lỗi & rate limit

- **Lỗi auth:** `error.code` 190 (token) / 200 (permission) → lấy token mới / kiểm tra quyền.
- **Lỗi giả 4xx:** kiểm tra lại có nhét token trực tiếp vào URL không → chuyển sang `curl -G --data-urlencode`.
- **Pagination:** response có `paging.next` → gọi tiếp URL đó tới khi hết.
- **Rate limit (429):** backoff 1s rồi tăng dần, tối đa 5 lần retry.
- **Bắt buộc tiền tố `act_`** khi gọi bằng ad account ID.

## 6. Lưu ý khi viết báo cáo cho người dùng

- Viết dạng **văn xuôi/bullet gọn**, hạn chế bảng biểu nếu người dùng khó đọc bảng.
- Nêu rõ **số nào lấy từ đâu** (account/campaign level), **đơn vị VNĐ** nếu tiền tệ VND.
- Số tự tính (CP/lượt mua, ROAS, CP/tin nhắn) phải ghi rõ là **tự tính**, không phải số Meta trả về.
- Thiếu dữ liệu → nói thẳng "chưa có / = 0", KHÔNG bịa.
