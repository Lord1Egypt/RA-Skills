---
name: "meta-ads-report"
description: "Kéo báo cáo chỉ số Meta Ads (Facebook/Instagram) qua Graph API. Đọc: insights, campaign, account, kiểm tra hạn token. Ghi: bật/tắt campaign-adset-ad (có xác nhận + dry-run)."
---

# Meta Ads Report + Control

Kéo chỉ số báo cáo quảng cáo Meta qua **Graph API chính thức** bằng HTTP (curl) — không cần SDK. Kèm 1 nhóm lệnh **ghi duy nhất: bật/tắt (ACTIVE/PAUSED)** campaign / adset / ad.

> 🔒 **Giới hạn ghi của skill này (đọc kỹ trước khi làm):**
> - **CHỈ được đổi `status`** giữa `ACTIVE` và `PAUSED`. Không làm gì khác.
> - **KHÔNG BAO GIỜ gọi DELETE/archive.** Không đổi ngân sách, bid, target, audience, creative, lịch chạy.
> - **KHÔNG tạo** campaign/adset/ad mới.
> - Mọi lệnh ghi PHẢI qua 2 bước: **dry-run in danh sách → người dùng xác nhận → mới gọi thật**. Không tự động tắt/bật theo cảm tính.
> - Mục 1–6 (đọc báo cáo, chỉ số, xử lý lỗi) vẫn là READ-ONLY tuyệt đối.

## 1. Cấu hình (environment variables)

| Biến | Bắt buộc | Mô tả |
|------|----------|-------|
| `META_ACCESS_TOKEN` | ✅ | Meta access token (User token hoặc System User token). Đọc báo cáo: `ads_read`. Bật/tắt quảng cáo: **cần thêm `ads_management`** |
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

## 7. Bật / tắt quảng cáo (nhóm lệnh GHI duy nhất)

### 7.1 Kiểm tra quyền trước khi làm

```bash
curl -s -G "https://graph.facebook.com/v21.0/debug_token" \
  --data-urlencode "input_token=$META_ACCESS_TOKEN" \
  --data-urlencode "access_token=$META_ACCESS_TOKEN" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data'].get('scopes'))"
```

- Không thấy `ads_management` → **báo thẳng với người dùng là chưa bật/tắt được**, không thử rồi báo lỗi mơ hồ.
- Cách lấy quyền: token mới ở Explorer có tick `ads_read` + `ads_management` (mục 2).

### 7.2 Xem trạng thái hiện tại (GET — luôn làm bước này trước)

```bash
# campaign
curl -s -G "https://graph.facebook.com/v21.0/act_$META_AD_ACCOUNT_ID/campaigns" \
  --data-urlencode "fields=id,name,status,effective_status,objective,daily_budget" \
  --data-urlencode "limit=200" \
  --data-urlencode "access_token=$META_ACCESS_TOKEN"

# adset trong 1 campaign
curl -s -G "https://graph.facebook.com/v21.0/{CAMPAIGN_ID}/adsets" \
  --data-urlencode "fields=id,name,status,effective_status,daily_budget" \
  --data-urlencode "access_token=$META_ACCESS_TOKEN"

# ad trong 1 adset
curl -s -G "https://graph.facebook.com/v21.0/{ADSET_ID}/ads" \
  --data-urlencode "fields=id,name,status,effective_status" \
  --data-urlencode "access_token=$META_ACCESS_TOKEN"
```

**`status` vs `effective_status` — phân biệt rất quan trọng:**

| Field | Nghĩa |
|---|---|
| `status` | Trạng thái **do người dùng đặt**: `ACTIVE` / `PAUSED` / `ARCHIVED` / `DELETED` |
| `effective_status` | Trạng thái **thực tế đang chạy**, tính cả cấp cha + lỗi hệ thống |

Bảng đọc `effective_status` hay gặp:

| Giá trị | Nghĩa | Muốn chạy lại thì phải |
|---|---|---|
| `ACTIVE` | Đang chạy | — |
| `PAUSED` | Bị tạm dừng ở chính nó | bật chính nó |
| `CAMPAIGN_PAUSED` | Camp cha đang PAUSED | bật campaign |
| `ADSET_PAUSED` | Adset cha đang PAUSED | bật adset |
| `PENDING_REVIEW` | Đang chờ Meta duyệt | chờ |
| `DISAPPROVED` | Bị từ chối | sửa creative (ngoài skill này) |
| `WITH_ISSUES` | Có lỗi thanh toán/chính sách | xử lý ở TKQC (ngoài skill này) |
| `ACCOUNT_DISABLED` / `ACCOUNT_PENDING_RISK_REVIEW` | TKQC bị khoá/đang xét | không bật được bằng API |
| `CAMPAIGN_ENDED` / `ADSET_ENDED` | Hết lịch chạy | đổi lịch (ngoài skill này) |

→ Khi người dùng nói "camp không chạy, bật lại", **luôn đọc `effective_status` trước** để biết bật ở cấp nào. Bật camp mà adset vẫn PAUSED → vẫn không chạy.

### 7.3 Lệnh bật / tắt (POST — bắt buộc qua xác nhận)

```bash
# tắt
curl -s -X POST "https://graph.facebook.com/v21.0/{OBJECT_ID}" \
  --data-urlencode "status=PAUSED" \
  --data-urlencode "access_token=$META_ACCESS_TOKEN"

# bật
curl -s -X POST "https://graph.facebook.com/v21.0/{OBJECT_ID}" \
  --data-urlencode "status=ACTIVE" \
  --data-urlencode "access_token=$META_ACCESS_TOKEN"
```

`{OBJECT_ID}` là id campaign, adset hoặc ad. Trả về `{"success": true}` là đã nhận.

**Bắt buộc với MỌI lệnh ghi — quy trình 5 bước:**

1. **Xác định đối tượng chính xác:** id + tên + cấp (campaign/adset/ad) + TKQC. Không dùng tên mơ hồ — nếu tên trùng thì liệt kê id cho người dùng chọn.
2. **Dry-run:** in ra bảng "sẽ đổi: [id] [tên] [cấp] [TKQC] trạng thái hiện tại → trạng thái mới". **Chưa gọi POST.**
3. **Chờ xác nhận rõ ràng** của người dùng ("ok tắt", "đồng ý"...). Không suy ra từ câu nói chung chung.
4. **Gọi POST** đúng số object đã duyệt.
5. **Đọc lại trạng thái** (`status` + `effective_status`) làm bằng chứng, báo lại kèm id.

**Không được làm:**
- Tắt/bật hàng loạt > 5 object trong 1 lần mà không liệt kê đủ danh sách cho người dùng duyệt.
- Tự bật lại camp người dùng đã tắt hôm trước (vd camp LIVE nghỉ theo ngày — xem mục 6 ghi chú báo cáo).
- Gọi POST khi chưa có `ads_management` → sẽ lỗi 200/OAuthException; kiểm ở 7.1 trước.
- Dùng `DELETE` hay `status=ARCHIVED` để "tắt cho gọn" — mất dữ liệu lịch sử, không khôi phục được như PAUSED.

### 7.4 Lỗi hay gặp khi bật/tắt

| Lỗi | Nguyên nhân | Xử lý |
|---|---|---|
| `(#200) Permissions error` | Token thiếu `ads_management` | lấy token mới (7.1) |
| `(#100) Invalid parameter` | id sai / đổi `status` ở object đã ARCHIVED | kiểm id, không tự ý bỏ archive |
| `(#2635) You are calling a deprecated version` | sai version Graph API | dùng `v21.0` |
| Bật ACTIVE mà `effective_status` vẫn `ADSET_PAUSED` | cấp cha đang tắt | bật ở cấp cha trước |
| Bật ACTIVE mà vẫn `WITH_ISSUES` | lỗi thanh toán/chính sách | báo người dùng — API không sửa được |
