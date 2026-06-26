# PLAN_A_TEST.md

# Plan A — Deep Test Plan

Mục tiêu: kiểm thử thật kỹ workflow báo cáo sinh nhật + ngày đặc biệt từ Google Sheets sang Discord.

## 1. Scope

Nguồn dữ liệu:
- Tab `Trang tính1`: nhân sự / ngày sinh
- Tab `NgayDacBiet`: ngày lễ / sự kiện đặc biệt

Đầu ra:
- 1 báo cáo tự động lúc 07:00 sáng mỗi ngày
- gửi vào Discord channel `1483444824895000697`

Rule hiện tại:
- Nhắc trước 3 ngày
- So sánh sinh nhật theo ngày/tháng
- Event đặc biệt đọc theo `Ngày diễn ra`

---

## 2. Mục tiêu kiểm thử

Cần xác nhận 6 nhóm chính:
1. Đọc sheet đúng
2. Parse ngày đúng
3. Tính ngày nhắc đúng
4. Render báo cáo đúng
5. Xử lý dữ liệu bẩn / thiếu / sai đúng cách
6. Không nhắc sai, không nhắc trùng, không bỏ sót

---

## 3. Ma trận test tổng quát

### A. Sheet access / structure
- đọc được tab `Trang tính1`
- đọc được tab `NgayDacBiet`
- thiếu tab thì báo lỗi rõ ràng
- thiếu cột bắt buộc thì báo lỗi rõ ràng
- đổi thứ tự cột nhưng giữ đúng tên cột vẫn hoạt động
- thừa cột không làm hỏng workflow

### B. Date parsing
- parse `dd/MM/yyyy` đúng
- parse ngày có số 0 đầu đúng
- parse ngày text vs cell date đúng
- phát hiện ngày lỗi/không hợp lệ
- xử lý năm nhuận
- xử lý qua tháng / qua năm đúng

### C. Birthday logic
- sinh nhật hôm nay
- sinh nhật sau 1 ngày
- sinh nhật sau 2 ngày
- sinh nhật sau 3 ngày
- sinh nhật sau 4 ngày thì không nhắc
- sinh nhật đã qua thì không nhắc
- sinh nhật cuối năm -> đầu năm vẫn tính đúng
- nhiều người cùng sinh nhật cùng ngày

### D. Special event logic
- event hôm nay
- event sau 1/2/3 ngày
- event sau 4 ngày không nhắc
- event inactive không hiển thị
- event có remind_before_days riêng
- event cùng ngày với birthday
- nhiều event cùng ngày

### E. Output / Discord report
- format dễ đọc
- nhóm đúng thành hôm nay / sắp tới / cần chuẩn bị
- không lặp người / lặp event
- không rỗng bất thường
- khi không có dữ liệu thì báo “không có gì” đúng
- text Unicode tiếng Việt hiển thị đúng

### F. Robustness
- ô trống
- hàng trống giữa sheet
- tên có dấu
- bộ phận có ký tự lạ
- sheet lớn
- dữ liệu trùng
- dữ liệu sai định dạng

---

## 4. Bộ test case chi tiết

## 4.1. Test dữ liệu chuẩn (happy path)

### TC-A1 — 1 sinh nhật hôm nay
Input:
- 1 nhân sự có ngày sinh trùng ngày hiện tại
Expected:
- báo cáo mục “Hôm nay” có đúng tên người đó
- không xuất hiện ở mục “3 ngày tới” nữa

### TC-A2 — 1 sinh nhật sau 3 ngày
Input:
- 1 nhân sự có sinh nhật sau đúng 3 ngày
Expected:
- xuất hiện ở mục “Trong 3 ngày tới”
- nêu đúng số ngày còn lại nếu format có hiển thị

### TC-A3 — 1 event hôm nay
Input:
- 1 dòng `NgayDacBiet` có ngày diễn ra là hôm nay, active TRUE
Expected:
- báo cáo có event đó ở mục hôm nay

### TC-A4 — 1 event sau 3 ngày
Input:
- event sau 3 ngày, active TRUE
Expected:
- xuất hiện ở mục sắp tới

### TC-A5 — birthday + event cùng ngày
Input:
- 1 sinh nhật hôm nay
- 1 event hôm nay
Expected:
- báo cáo hiển thị đủ cả 2 loại
- không bỏ sót một bên nào

---

## 4.2. Test ranh giới ngày (boundary)

### TC-B1 — sau 4 ngày
Input:
- sinh nhật hoặc event sau 4 ngày
Expected:
- không xuất hiện trong báo cáo

### TC-B2 — hôm qua
Input:
- sinh nhật / event đã qua 1 ngày
Expected:
- không xuất hiện

### TC-B3 — cuối tháng
Input:
- hôm nay 28/02 hoặc 30/04, item rơi sang tháng sau trong 3 ngày tới
Expected:
- vẫn nhắc đúng

### TC-B4 — cuối năm
Input:
- giả lập ngày hiện tại 30/12 hoặc 31/12
- sinh nhật 01/01 hoặc 02/01
Expected:
- vẫn được tính là sắp tới

### TC-B5 — năm nhuận
Input:
- dữ liệu có 29/02/2000
Expected:
- cần xác định rule rõ:
  - chỉ nhắc vào năm nhuận
  - hoặc map sang 28/02 / 01/03 ở năm thường
Ghi chú:
- cần chốt rule trước khi đưa production

---

## 4.3. Test format ngày

### TC-C1 — đúng format dd/MM/yyyy
Expected:
- parse thành công

### TC-C2 — format d/M/yyyy
Input:
- 3/9/2003
Expected:
- nếu hỗ trợ thì parse được; nếu không hỗ trợ thì báo invalid rõ ràng

### TC-C3 — format sai hoàn toàn
Input:
- `2003-12-03`
Expected:
- không làm crash job
- ghi log hàng lỗi
- bỏ qua dòng lỗi

### TC-C4 — text không phải ngày
Input:
- `abcxyz`
Expected:
- bỏ qua dòng lỗi, có log

### TC-C5 — ngày không tồn tại
Input:
- `31/02/2001`
Expected:
- đánh dấu invalid

---

## 4.4. Test dữ liệu nhân sự

### TC-D1 — tên có dấu tiếng Việt
Input:
- `Nguyễn Vĩnh Tâm`
Expected:
- hiển thị đúng dấu

### TC-D2 — tên rất dài
Expected:
- báo cáo vẫn đọc được, không vỡ format

### TC-D3 — trùng tên khác mã NV
Input:
- 2 người cùng tên, khác mã
Expected:
- nếu cùng sinh nhật thì hiển thị đủ 2 người, không gộp nhầm

### TC-D4 — trùng mã NV
Expected:
- nên log cảnh báo duplicate
- không crash

### TC-D5 — dòng thiếu ngày sinh
Expected:
- bỏ qua dòng đó, log rõ lý do

### TC-D6 — dòng thiếu họ tên
Expected:
- bỏ qua dòng đó, log rõ

### TC-D7 — có nhân sự nghỉ việc nhưng vẫn nằm sheet
Expected:
- cần rule tương lai: thêm cột Active
- hiện tại nếu chưa có cột này thì vẫn sẽ bị tính

---

## 4.5. Test dữ liệu event

### TC-E1 — active FALSE
Expected:
- không hiển thị trong báo cáo

### TC-E2 — thiếu `Nhắc trước`
Expected:
- fallback về default = 3

### TC-E3 — `Nhắc trước` = 7
Expected:
- nếu logic hỗ trợ theo từng event thì event có thể xuất hiện sớm hơn
- nếu bản đầu đang global=3 thì cần log rằng field này chưa được áp dụng đầy đủ

### TC-E4 — thiếu tên sự kiện
Expected:
- bỏ qua, log lỗi

### TC-E5 — thiếu ngày diễn ra
Expected:
- bỏ qua, log lỗi

### TC-E6 — nhiều event cùng ngày
Expected:
- tất cả đều hiển thị

---

## 4.6. Test sheet layout / dirty data

### TC-F1 — có hàng trống giữa dữ liệu
Expected:
- job không dừng sớm sai cách

### TC-F2 — có khoảng trắng đầu/cuối ở tên
Input:
- `  Nguyễn Vĩnh Duy  `
Expected:
- trim trước khi render

### TC-F3 — cột `Vị trí ` có khoảng trắng cuối như hiện tại
Expected:
- mapping vẫn đúng nếu đang dùng tên cột linh hoạt hoặc index đúng

### TC-F4 — thêm cột mới ở giữa sheet
Expected:
- nếu mapping theo header name thì vẫn chạy
- nếu mapping theo index cố định thì có nguy cơ lỗi

### TC-F5 — sheet đổi tên tab
Expected:
- bot phải báo lỗi cấu hình rõ ràng

---

## 4.7. Test output báo cáo

### TC-G1 — không có gì hôm nay / 3 ngày tới
Expected:
- báo cáo ngắn gọn:
  - không có sinh nhật
  - không có ngày đặc biệt

### TC-G2 — có 1 item mỗi loại
Expected:
- format rõ ràng, tách mục hợp lý

### TC-G3 — có nhiều item
Expected:
- thứ tự nên tăng dần theo ngày
- cùng ngày thì group lại

### TC-G4 — text rất dài ở ghi chú
Expected:
- có thể cắt bớt / xuống dòng hợp lý

### TC-G5 — Unicode tiếng Việt
Expected:
- không lỗi encoding

---

## 4.8. Test idempotency / duplicate prevention

### TC-H1 — job chạy 2 lần cùng ngày
Expected:
- cần rule chống gửi trùng
- ví dụ ghi trạng thái last_sent_date

### TC-H2 — retry sau lỗi tạm thời
Expected:
- nếu retry, không spam 2 báo cáo giống nhau

### TC-H3 — bot restart gần giờ chạy
Expected:
- không bỏ sót báo cáo, không double-send

---

## 4.9. Test performance

### TC-I1 — 100 nhân sự
Expected:
- phản hồi nhanh, kết quả đúng

### TC-I2 — 1,000 nhân sự
Expected:
- vẫn xử lý ổn trong thời gian hợp lý

### TC-I3 — 200 event
Expected:
- render đúng, không timeout

---

## 4.10. Test lỗi hệ thống

### TC-J1 — mất quyền đọc sheet
Expected:
- báo lỗi rõ ràng
- không gửi báo cáo sai/trống như thể thành công

### TC-J2 — sheet bị xóa tab `NgayDacBiet`
Expected:
- báo cảnh báo phần event unavailable
- vẫn có thể báo birthday nếu tab nhân sự còn

### TC-J3 — Discord gửi thất bại
Expected:
- log lỗi gửi
- có cơ chế retry hoặc cảnh báo admin

### TC-J4 — Google API timeout
Expected:
- log rõ timeout
- không crash pipeline toàn bộ

---

## 5. Bộ dữ liệu test khuyến nghị

## 5.1. Dữ liệu nhân sự nên có thêm

Nên thêm các dòng test sau:
- 1 người sinh nhật hôm nay
- 1 người sinh nhật ngày mai
- 1 người sinh nhật sau 2 ngày
- 1 người sinh nhật sau 3 ngày
- 1 người sinh nhật sau 4 ngày
- 2 người cùng sinh nhật cùng ngày
- 1 dòng thiếu ngày sinh
- 1 dòng ngày sinh sai format
- 1 dòng tên trống
- 1 dòng 29/02
- 1 dòng cuối năm 31/12
- 1 dòng đầu năm 01/01

## 5.2. Dữ liệu event nên có thêm

Nên thêm các event test sau:
- 1 event hôm nay
- 1 event sau 1 ngày
- 1 event sau 3 ngày
- 1 event sau 4 ngày
- 1 event inactive FALSE
- 1 event thiếu ngày
- 1 event thiếu tên
- 2 event cùng ngày
- 1 event có `Nhắc trước = 7`

---

## 6. Tiêu chí pass/fail

Pass khi:
- đọc đúng tất cả item hợp lệ
- bỏ qua item lỗi mà không crash
- không gửi sai ngày
- không bỏ sót item trong cửa sổ 3 ngày
- message Discord rõ ràng, dễ đọc
- không gửi trùng khi job chạy lặp

Fail khi:
- parse sai ngày
- nhắc item >3 ngày
- bỏ sót item trong 0..3 ngày
- crash vì 1 dòng dữ liệu bẩn
- gửi report rỗng dù có dữ liệu hợp lệ

---

## 7. Ưu tiên test theo thứ tự

### Priority 1 — bắt buộc
- happy path birthday today
- birthday +1/+2/+3 day
- event today / +3 day
- no data case
- invalid date case
- missing field case
- duplicate prevention

### Priority 2 — nên test
- month boundary
- year boundary
- multiple items same day
- Unicode / trim spaces
- inactive event

### Priority 3 — test sâu
- leap year
- large dataset
- retry / timeout / Discord failure
- rename tab / column drift

---

## 8. Kết luận

Plan A tưởng đơn giản nhưng dễ sai ở 5 chỗ:
1. parse ngày
2. boundary cuối tháng/cuối năm
3. dữ liệu bẩn trong sheet
4. gửi trùng báo cáo
5. event inactive / thiếu field

Nếu muốn production ổn, nên test theo bộ case trên trước khi mở tự động hoàn toàn.
