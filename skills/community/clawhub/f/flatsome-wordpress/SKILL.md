# 🦞 FLATSOME MASTER SKILL — AI Web Designer
# Dành cho OpenClaw & mọi AI Agent

> **Nhiệm vụ tối thượng:** Nhận ảnh mẫu / URL / mô tả từ người dùng → Phân tích từng pixel
> → Tái tạo 100% bằng UXBuilder shortcode + CSS. **KHÔNG dùng HTML thô.**
> Output hoàn chỉnh, production-ready, không cần chỉnh sửa lại.

---

## ═══ PHẦN 0 — NGUYÊN TẮC BẤT BIẾN ═══

### 0.1 Kim Chỉ Nam Khi Nhận Mẫu

Khi người dùng gửi ảnh / screenshot / URL mẫu, AI phải:

```
BƯỚC 1: PHÂN TÍCH VISUAL
  ├── Đếm số section từ trên xuống dưới
  ├── Xác định layout mỗi section (1 cột / 2 cột / 3 cột / full-width)
  ├── Nhận diện màu sắc chủ đạo (hex)
  ├── Đọc font size tương đối (h1 / h2 / h3 / body)
  ├── Nhận diện component: hero / features / testimonial / pricing / FAQ / CTA
  └── Ghi chú animation / hover effect nếu có

BƯỚC 2: LẬP BẢN ĐỒ SHORTCODE
  ├── Mỗi section → shortcode wrapper tương ứng
  ├── Mỗi element → shortcode con tương ứng
  └── CSS tùy chỉnh → gom vào 1 block cuối

BƯỚC 3: XUẤT CODE HOÀN CHỈNH
  ├── Shortcode đầy đủ, có thể paste ngay vào WP
  ├── CSS bổ sung kèm theo
  └── Hướng dẫn thay IMAGE_ID / FORM_ID / màu sắc
```

### 0.2 Hệ Thống Ưu Tiên UX-FIRST (Bất Biến)

```
Cấp 1 ▶ Shortcode UXBuilder thuần                 → LUÔN dùng trước
Cấp 2 ▶ Shortcode UXBuilder + class CSS           → Khi cần style đặc biệt
Cấp 3 ▶ [ux_html] với HTML tối thiểu              → Khi không có shortcode thay thế
Cấp 4 ▶ WPCode PHP snippet                        → Logic động, hook, filter
Cấp 5 ▶ functions.php trong child theme           → Chỉ khi không còn lựa chọn
```

**TUYỆT ĐỐI CẤM:**
- ❌ `<div>`, `<p>`, `<h1-h6>`, `<a>`, `<img>` đứng riêng ngoài `[ux_html]`
- ❌ `style="..."` inline khi có thể dùng attribute shortcode
- ❌ Sửa file trong `/themes/flatsome/` — luôn dùng `flatsome-child`
- ❌ Nhiều WPCode snippet cho cùng 1 mục đích
- ❌ Import framework CSS ngoài (Bootstrap, Tailwind) — Flatsome đã có grid riêng

### 0.3 Quy Trình Thực Thi Chuẩn

```
[Nhận yêu cầu + mẫu]
       │
       ▼
[Phân tích] → Loại site, màu brand, font, sections, components
       │
       ▼
[Môi trường] → WP-CLI setup, child theme, plugins
       │
       ▼
[Build shortcode] → Từng trang, từng section, từng element
       │
       ▼
[CSS bổ sung] → Chỉ những gì shortcode không làm được
       │
       ▼
[Menu + Header + Footer] → Cấu hình hoàn chỉnh
       │
       ▼
[Báo cáo] → URL, checklist, hướng dẫn chỉnh sửa
```

---

## ═══ PHẦN 1 — MÔI TRƯỜNG & CÀI ĐẶT ═══

### 1.1 WP-CLI Setup

```bash
# LocalWP macOS Apple Silicon (M1/M2/M3/M4)
export WP_CLI_PHP="/Applications/Local.app/Contents/Resources/extraResources/lightning-services/php-8.2.29+0/bin/darwin-arm64/bin/php"

# LocalWP macOS Intel
export WP_CLI_PHP="/Applications/Local.app/Contents/Resources/extraResources/lightning-services/php-8.2.29+0/bin/darwin-x64/bin/php"

# LocalWP Windows (WSL)
export WP_CLI_PHP="/mnt/c/Users/USERNAME/AppData/Roaming/Local/lightning-services/php-8.2.29+0/bin/win32/php.exe"

# Hosting thật (cPanel / SSH)
# WP-CLI thường đã có sẵn, chỉ cần: wp --info

# Xác nhận
wp core version && wp theme list --status=active
```

### 1.2 Tạo Child Theme (BẮT BUỘC)

```bash
THEMES_DIR=$(wp eval "echo get_theme_root();")
mkdir -p "$THEMES_DIR/flatsome-child"

# style.css
cat > "$THEMES_DIR/flatsome-child/style.css" << 'CSS'
/*
Theme Name:   Flatsome Child
Template:     flatsome
Version:      1.0.0
Description:  Child theme for Flatsome
*/
@import url("../flatsome/style.css");
CSS

# functions.php
cat > "$THEMES_DIR/flatsome-child/functions.php" << 'PHP'
<?php
add_action('wp_enqueue_scripts', function() {
    wp_enqueue_style('flatsome-parent', get_template_directory_uri() . '/style.css');
    wp_enqueue_style('flatsome-child', get_stylesheet_uri(), ['flatsome-parent']);
}, 20);
PHP

wp theme activate flatsome-child
echo "Child theme activated!"
```

### 1.3 Plugin Cần Thiết

```bash
# Cốt lõi
wp plugin install contact-form-7 --activate        # CF7 form
wp plugin install wpcode-lite --activate            # Code snippets
wp plugin install classic-editor --activate         # Editor ổn định

# Tùy chọn theo nhu cầu
wp plugin install woocommerce --activate            # Thương mại điện tử
wp plugin install wp-optimize --activate            # Cache + optimize
wp plugin install wordfence --activate              # Bảo mật
wp plugin install rank-math --activate              # SEO
wp plugin install elementor --activate              # Nếu cần builder thêm
```

### 1.4 Theme Options Flatsome

```bash
# Màu sắc brand
wp option patch update flatsome_options color_primary "#YOUR_PRIMARY"
wp option patch update flatsome_options color_secondary "#YOUR_SECONDARY"
wp option patch update flatsome_options color_button "#YOUR_BUTTON_COLOR"

# Typography
wp option patch update flatsome_options google_font "Inter"
wp option patch update flatsome_options google_font_size "16"
wp option patch update flatsome_options google_font_weight "400"
wp option patch update flatsome_options heading_font "Poppins"

# Header
wp option patch update flatsome_options header_width "full-width"
wp option patch update flatsome_options header_bg "#ffffff"
wp option patch update flatsome_options sticky_header "1"
wp option patch update flatsome_options header_transparent "1"   # header trong suốt

# Footer
wp option patch update flatsome_options footer_copyright "© 2026 Tên Công Ty."
wp option patch update flatsome_options footer_background "#1a1a2e"
wp option patch update flatsome_options footer_text_color "#aaaaaa"

# Performance
wp option patch update flatsome_options lazy_load_images "1"
wp option patch update flatsome_options minify_css "1"
wp option patch update flatsome_options minify_js "1"
```

---

## ═══ PHẦN 2 — TOÀN BỘ SHORTCODE UXBUILDER ═══

### 2.1 Khung Layout Cơ Bản

**Section (Wrapper ngoài cùng):**
```
[section
  bg=""                  → ID ảnh nền WP
  bg_color=""            → Màu nền: "#fff" | "rgba(0,0,0,0.5)" | "var(--color-primary)"
  bg_overlay=""          → Lớp phủ: "rgba(0,0,0,0.5)"
  bg_pos=""              → "center center" | "top left" | "50% 30%"
  bg_size=""             → "cover" | "contain" | "auto"
  bg_fixed="1"           → Parallax scrolling
  padding=""             → "80px 0" | "60px" | "40px 0 60px"
  padding__sm=""         → Padding mobile: "40px 0"
  margin=""              → Margin ngoài
  text_color=""          → "light" | "dark"
  border=""              → "top" | "bottom" | "top bottom"
  border_color=""        → "#eee"
  class=""               → CSS class tùy chỉnh
  visibility=""          → "hidden--mobile" | "hidden--tablet" | "show--mobile"
]
```

**Row (Hàng ngang):**
```
[row
  width=""               → "full-width" | "custom" | (bỏ trống = boxed)
  custom_width=""        → "1200px" (khi width="custom")
  h_align=""             → "left" | "center" | "right"
  v_align=""             → "top" | "middle" | "bottom"
  gap=""                 → "small" | "large" | "collapse"
  col_bg=""              → Màu nền cho toàn row
]
```

**Col (Cột):**
```
[col
  span=""                → 1–12 (12 = full width)
  span__sm=""            → Mobile: thường "12"
  span__md=""            → Tablet
  push=""                → Đẩy phải (1-11)
  pull=""                → Đẩy trái
  padding=""             → Padding riêng
  align=""               → "left" | "center" | "right"
  bg_color=""            → Màu nền riêng cột
  class=""               → CSS class
  visibility=""          → "hidden--mobile"
]
```

**Row lồng trong Col (inner):**
```
[row_inner] [col_inner span="6" span__sm="12"] ... [/col_inner] [/row_inner]
```

---

### 2.2 Hero & Banner — Clone Từ Mẫu

**Hero Banner Tĩnh (Full Screen):**
```
[ux_banner
  bg="IMAGE_ID"
  bg_overlay="rgba(20,20,20,0.55)"
  height="100vh"
  height__sm="80vh"
  bg_pos="center center"
  bg_size="cover"
  class="hero-main"
]
  [text_box
    width="65"
    width__sm="92"
    position_x="50"
    position_y="50"
    text_align="center"
    animate="fadeInUp"
  ]
    [ux_text font_size="14px" text_color="rgba(255,255,255,0.7)" class="hero-label"]
      ✦ THƯƠNG HIỆU / TAGLINE NGẮN
    [/ux_text]
    [gap height="12px"]
    [ux_text_box_title font_size="h1" class="hero-title"]
      Dòng Tiêu Đề Chính Mạnh Mẽ
      Hai Dòng Gây Ấn Tượng
    [/ux_text_box_title]
    [gap height="16px"]
    [ux_text font_size="18px" text_color="rgba(255,255,255,0.85)" class="hero-sub"]
      Mô tả giá trị cốt lõi — rõ ràng, súc tích, tập trung vào lợi ích khách hàng nhận được.
    [/ux_text]
    [gap height="28px"]
    [button text="Bắt Đầu Ngay" link="/lien-he/" size="xlarge" radius="99"
      color="var(--color-primary)" icon="fas fa-arrow-right" icon_pos="right"]
    [gap height="0" height__sm="8px"]
    [button text="Xem Portfolio" link="/du-an/" size="xlarge" radius="99"
      style="outline" color="rgba(255,255,255,0.85)"]
    [gap height="32px"]
    [ux_text font_size="13px" text_color="rgba(255,255,255,0.6)"]
      ★★★★★ Hơn 500 khách hàng tin tưởng · Bảo hành 12 tháng · Hỗ trợ 24/7
    [/ux_text]
  [/text_box]
[/ux_banner]
```

**Hero Slider (Đa Slide):**
```
[ux_slider
  arrows="true"
  bullets="true"
  autoplay="5"
  height="680px"
  height__sm="420px"
  slide_show="1"
  transition="fade"
]
  [ux_banner bg="IMAGE_ID_1" bg_overlay="rgba(0,0,0,0.45)" height="680px" height__sm="420px"]
    [text_box width="60" width__sm="90" position_x="50" position_y="55" text_align="center" animate="fadeInUp"]
      [ux_text_box_title font_size="h1"]Slide 1 — Tiêu Đề Chính[/ux_text_box_title]
      [ux_text]Mô tả slide 1 — giá trị hoặc khuyến mãi đặc biệt[/ux_text]
      [button text="Khám Phá Ngay" link="#" size="large" radius="99"]
    [/text_box]
  [/ux_banner]
  [ux_banner bg="IMAGE_ID_2" bg_overlay="rgba(0,40,80,0.55)" height="680px" height__sm="420px"]
    [text_box width="55" width__sm="90" position_x="20" position_y="50" animate="fadeInLeft"]
      [ux_text_box_title font_size="h1"]Slide 2 — Tiêu Đề Khác[/ux_text_box_title]
      [ux_text]Mô tả slide 2[/ux_text]
      [button text="Tìm Hiểu Thêm" link="#" size="large" radius="99"]
    [/text_box]
  [/ux_banner]
[/ux_slider]
```

**Hero Split 2 Cột (Text Trái + Ảnh Phải):**
```
[section bg_color="#f8f9fa" padding="100px 0" padding__sm="60px 0"]
  [row v_align="middle" h_align="center"]
    [col span="6" span__sm="12" padding="0 40px 0 0" padding__sm="0"]
      [ux_text font_size="13px" text_color="var(--color-primary)" class="eyebrow-label"]
        ✦ CATEGORY / BADGE
      [/ux_text]
      [gap height="12px"]
      [ux_text font_size="h1"]
        ## Tiêu Đề Lớn
        ## Hai Dòng Ở Đây
      [/ux_text]
      [gap height="16px"]
      [ux_text font_size="17px" line_height="1.8" text_color="rgba(0,0,0,0.65)"]
        Đoạn mô tả chi tiết, tập trung vào lợi ích người dùng nhận được. Viết thật rõ ràng và đáng tin cậy.
      [/ux_text]
      [gap height="12px"]
      [row_inner]
        [col_inner span="auto"]
          [ux_feature_box pos="left" icon="fas fa-check-circle" icon_color="var(--color-primary)" icon_size="20"]
            Lợi ích / Tính năng 1
          [/ux_feature_box]
        [/col_inner]
        [col_inner span="auto"]
          [ux_feature_box pos="left" icon="fas fa-check-circle" icon_color="var(--color-primary)" icon_size="20"]
            Lợi ích / Tính năng 2
          [/ux_feature_box]
        [/col_inner]
      [/row_inner]
      [gap height="28px"]
      [button text="Dùng Thử Miễn Phí" link="#" size="large" radius="99" color="var(--color-primary)"]
      [button text="Xem Demo" link="#" size="large" radius="99" style="outline"]
    [/col]
    [col span="6" span__sm="12"]
      [ux_image id="IMAGE_ID" image_size="large" shadow="3" animate="fadeInRight" radius="12"]
    [/col]
  [/row]
[/section]
```

---

### 2.3 Typography & Text Elements

**Section Title Chuẩn:**
```
[section padding="70px 0"]
  [row h_align="center"]
    [col span="8" span__sm="12" align="center"]
      [ux_text font_size="13px" text_color="var(--color-primary)"]✦ SECTION LABEL[/ux_text]
      [gap height="8px"]
      [title text="Tiêu Đề Section Chính" tag="h2" text_align="center"]
      [gap height="8px"]
      [ux_text font_size="17px" text_color="rgba(0,0,0,0.6)" text_align="center"]
        Mô tả phụ rõ ràng, ngắn gọn dưới tiêu đề — 1–2 câu.
      [/ux_text]
    [/col]
  [/row]
  [gap height="48px"]
  ... nội dung section ...
[/section]
```

**Rich Text:**
```
[ux_text
  text_align="center"
  font_size="18px"
  line_height="1.8"
  text_color="rgba(0,0,0,0.7)"
  max_width="700px"
  margin="0 auto"
]
  Nội dung văn bản đầy đủ. Có thể dùng **bold**, *italic*, [link](url).
[/ux_text]
```

**Animated Counter (Số liệu):**
```
[section padding="60px 0" bg_color="#f8f9fa"]
  [row h_align="center"]
    [col span="3" span__sm="6" align="center"]
      [ux_counter num="500" suffix="+" text="Khách Hàng" font_size="h2" color="var(--color-primary)"]
    [/col]
    [col span="3" span__sm="6" align="center"]
      [ux_counter num="10" suffix="+" text="Năm Kinh Nghiệm" font_size="h2" color="var(--color-primary)"]
    [/col]
    [col span="3" span__sm="6" align="center"]
      [ux_counter num="98" suffix="%" text="Hài Lòng" font_size="h2" color="var(--color-primary)"]
    [/col]
    [col span="3" span__sm="6" align="center"]
      [ux_counter num="24" suffix="/7" text="Hỗ Trợ" font_size="h2" color="var(--color-primary)"]
    [/col]
  [/row]
[/section]
```

---

### 2.4 Feature Box & Icon Box

**Feature 3 Cột Icon Top (Phổ biến nhất):**
```
[section padding="80px 0"]
  [title text="Tại Sao Chọn Chúng Tôi" tag="h2" text_align="center"]
  [gap height="48px"]
  [row]
    [col span="4" span__sm="12" align="center"]
      [ux_feature_box pos="top" icon="fas fa-bolt" icon_color="var(--color-primary)"
        icon_size="48" icon_bg_color="rgba(var(--color-primary-rgb),0.1)" icon_radius="50%"
        text_align="center" class="feature-card"]
        [ux_feature_box_title]Tốc Độ Vượt Trội[/ux_feature_box_title]
        Triển khai trong 24 giờ, hiệu suất tối ưu trên mọi thiết bị và nền tảng.
      [/ux_feature_box]
    [/col]
    [col span="4" span__sm="12" align="center"]
      [ux_feature_box pos="top" icon="fas fa-shield-alt" icon_color="var(--color-primary)"
        icon_size="48" text_align="center" class="feature-card"]
        [ux_feature_box_title]Bảo Mật Tuyệt Đối[/ux_feature_box_title]
        Dữ liệu mã hóa SSL, sao lưu tự động 24/7, chứng chỉ quốc tế.
      [/ux_feature_box]
    [/col]
    [col span="4" span__sm="12" align="center"]
      [ux_feature_box pos="top" icon="fas fa-headset" icon_color="var(--color-primary)"
        icon_size="48" text_align="center" class="feature-card"]
        [ux_feature_box_title]Hỗ Trợ 24/7[/ux_feature_box_title]
        Đội ngũ chuyên gia luôn sẵn sàng, phản hồi trong vòng 30 phút.
      [/ux_feature_box]
    [/col]
  [/row]
[/section]
```

**Feature Icon Trái (Dạng list):**
```
[row]
  [col span="12"]
    [ux_feature_box pos="left" icon="fas fa-check" icon_color="var(--color-primary)" icon_size="24"]
      [ux_feature_box_title]Tính Năng Quan Trọng 1[/ux_feature_box_title]
      Mô tả chi tiết tính năng này, lợi ích cụ thể mà khách hàng nhận được.
    [/ux_feature_box]
    [gap height="20px"]
    [ux_feature_box pos="left" icon="fas fa-check" icon_color="var(--color-primary)" icon_size="24"]
      [ux_feature_box_title]Tính Năng Quan Trọng 2[/ux_feature_box_title]
      Mô tả tính năng thứ hai với con số cụ thể nếu có.
    [/ux_feature_box]
  [/col]
[/row]
```

**Step Process (Quy trình):**
```
[section padding="80px 0"]
  [title text="Quy Trình Làm Việc" tag="h2" text_align="center"]
  [gap height="48px"]
  [row h_align="center"]
    [col span="3" span__sm="6" align="center"]
      [ux_feature_box pos="top" icon="fas fa-search" icon_color="#fff"
        icon_bg_color="var(--color-primary)" icon_radius="50%" icon_size="36" text_align="center"]
        [ux_text font_size="12px" text_color="var(--color-primary)"]BƯỚC 01[/ux_text]
        [ux_feature_box_title]Tư Vấn & Phân Tích[/ux_feature_box_title]
        Hiểu rõ nhu cầu, mục tiêu và đối tượng khách hàng của bạn.
      [/ux_feature_box]
    [/col]
    [col span="3" span__sm="6" align="center"]
      [ux_feature_box pos="top" icon="fas fa-pencil-ruler" icon_color="#fff"
        icon_bg_color="var(--color-primary)" icon_radius="50%" icon_size="36" text_align="center"]
        [ux_text font_size="12px" text_color="var(--color-primary)"]BƯỚC 02[/ux_text]
        [ux_feature_box_title]Thiết Kế & Lên Kế Hoạch[/ux_feature_box_title]
        Wireframe, mockup và kế hoạch triển khai chi tiết.
      [/ux_feature_box]
    [/col]
    [col span="3" span__sm="6" align="center"]
      [ux_feature_box pos="top" icon="fas fa-code" icon_color="#fff"
        icon_bg_color="var(--color-primary)" icon_radius="50%" icon_size="36" text_align="center"]
        [ux_text font_size="12px" text_color="var(--color-primary)"]BƯỚC 03[/ux_text]
        [ux_feature_box_title]Phát Triển & Testing[/ux_feature_box_title]
        Code, kiểm thử đa nền tảng, tối ưu tốc độ.
      [/ux_feature_box]
    [/col]
    [col span="3" span__sm="6" align="center"]
      [ux_feature_box pos="top" icon="fas fa-rocket" icon_color="#fff"
        icon_bg_color="var(--color-primary)" icon_radius="50%" icon_size="36" text_align="center"]
        [ux_text font_size="12px" text_color="var(--color-primary)"]BƯỚC 04[/ux_text]
        [ux_feature_box_title]Bàn Giao & Hỗ Trợ[/ux_feature_box_title]
        Ra mắt và hỗ trợ bảo hành 12 tháng.
      [/ux_feature_box]
    [/col]
  [/row]
[/section]
```

---

### 2.5 Button & CTA

```
[button text="Nút Mặc Định" link="#"]
[button text="Nút Lớn Pill" link="#" size="large" radius="99"]
[button text="Nút Outline" link="#" style="outline" radius="5" size="large"]
[button text="Màu Tùy Chỉnh" link="#" color="#e74c3c" size="large" radius="99"]
[button text="Có Icon Trái" link="#" icon="fas fa-download" icon_pos="left"]
[button text="Có Icon Phải" link="#" icon="fas fa-arrow-right" icon_pos="right"]
[button text="Full Width" link="#" expand="true" size="large"]
[button text="Liên Kết Ngoài" link="https://..." target="_blank" rel="noopener"]
[button text="Ghost White" link="#" style="white" color="transparent" size="large"]
```

**CTA Bar Brand Color:**
```
[section bg_color="var(--color-primary)" text_color="light" padding="70px 0"]
  [row width="custom" custom_width="860px" h_align="center"]
    [col span="12" align="center"]
      [ux_text font_size="h2"]**Sẵn Sàng Bắt Đầu Cùng Chúng Tôi?**[/ux_text]
      [gap height="12px"]
      [ux_text font_size="16px" text_color="rgba(255,255,255,0.85)"]
        Tham gia cùng 500+ khách hàng đang tăng trưởng mạnh mẽ.
      [/ux_text]
      [gap height="24px"]
      [button text="Nhận Tư Vấn Miễn Phí" link="/lien-he/" size="xlarge" radius="99" style="white"]
      [button text="Xem Bảng Giá" link="/bang-gia/" size="xlarge" radius="99"
        style="outline" color="rgba(255,255,255,0.9)"]
    [/col]
  [/row]
[/section]
```

**CTA Section Gradient:**
```
[section class="cta-gradient" padding="80px 0" text_color="light"]
  [row h_align="center"]
    [col span="10" span__sm="12" align="center"]
      [ux_text font_size="h2"]Tiêu Đề CTA Cuối Trang[/ux_text]
      [gap height="16px"]
      [button text="Hành Động Ngay" link="#" size="xlarge" radius="99" style="white"]
    [/col]
  [/row]
[/section]
```
CSS đi kèm:
```css
.cta-gradient { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
```

---

### 2.6 Media — Ảnh, Gallery, Video

**Ảnh Đơn:**
```
[ux_image id="IMAGE_ID" image_size="large" shadow="2" radius="8" animate="fadeIn"]
[ux_image id="IMAGE_ID" image_size="full" link="#" lightbox="true"]
[ux_image id="IMAGE_ID" width="80" position_x="50"]
```

**Gallery Grid:**
```
[ux_gallery type="grid" columns="3" columns__sm="2" gap="small" lightbox="true" animate="fadeInUp"]
  [ux_gallery_item image="ID1" caption="Dự án 1"]
  [ux_gallery_item image="ID2" caption="Dự án 2"]
  [ux_gallery_item image="ID3" caption="Dự án 3"]
  [ux_gallery_item image="ID4"]
  [ux_gallery_item image="ID5"]
  [ux_gallery_item image="ID6"]
[/ux_gallery]
```

**Gallery Masonry (Portfolio):**
```
[ux_gallery type="masonry" columns="3" columns__sm="2" gap="small" lightbox="true"]
  [ux_gallery_item image="ID1"]
  [ux_gallery_item image="ID2"]
  [ux_gallery_item image="ID3"]
[/ux_gallery]
```

**Video YouTube / Vimeo:**
```
[ux_video url="https://www.youtube.com/watch?v=VIDEO_ID" width="900" ratio="16:9"]
```

**Video Testimonials 3 Cột:**
```
[section padding="70px 0" bg_color="#f8f9fa"]
  [title text="Khách Hàng Chia Sẻ" tag="h2" text_align="center"]
  [gap height="40px"]
  [row]
    [col span="4" span__sm="12"]
      [ux_video url="https://youtube.com/watch?v=ID1"]
      [gap height="8px"]
      [ux_text text_align="center" font_size="14px" text_color="rgba(0,0,0,0.6)"]
        Nguyễn Văn A — CEO, Công ty ABC
      [/ux_text]
    [/col]
    [col span="4" span__sm="12"]
      [ux_video url="https://youtube.com/watch?v=ID2"]
      [gap height="8px"]
      [ux_text text_align="center" font_size="14px" text_color="rgba(0,0,0,0.6)"]
        Trần Thị B — Founder, Startup XYZ
      [/ux_text]
    [/col]
    [col span="4" span__sm="12"]
      [ux_video url="https://youtube.com/watch?v=ID3"]
      [gap height="8px"]
      [ux_text text_align="center" font_size="14px" text_color="rgba(0,0,0,0.6)"]
        Lê Văn C — Giám đốc, Tập đoàn DEF
      [/ux_text]
    [/col]
  [/row]
[/section]
```

---

### 2.7 Testimonials & Social Proof

**Testimonial Slider:**
```
[section bg_color="#f8f9fa" padding="80px 0"]
  [title text="Khách Hàng Nói Gì Về Chúng Tôi" tag="h2" text_align="center"]
  [gap height="48px"]
  [ux_testimonials columns="3" columns__sm="1" slide_show="1" autoplay="1" gap="24px"]
    [testimonial name="Nguyễn Minh Tuấn" position="Giám đốc — Công ty ABC"
      img="IMAGE_ID" star_rating="5"]
      Dịch vụ tuyệt vời! Đội ngũ chuyên nghiệp và tận tâm. Kết quả vượt xa mong đợi
      của chúng tôi sau 3 tháng hợp tác. Chắc chắn sẽ tiếp tục dài hạn.
    [/testimonial]
    [testimonial name="Trần Thu Hương" position="CEO — Startup Fintech XYZ"
      img="IMAGE_ID" star_rating="5"]
      Tiến độ nhanh, chất lượng hoàn hảo. Mình đã thử 3 đơn vị khác trước đây
      nhưng chỉ ở đây mới thực sự hài lòng. Rất recommend!
    [/testimonial]
    [testimonial name="Phạm Hoàng Long" position="Chủ doanh nghiệp SME"
      img="IMAGE_ID" star_rating="5"]
      Giá cả hợp lý, hỗ trợ nhiệt tình 24/7. Họ hiểu rõ nhu cầu của mình
      ngay từ buổi tư vấn đầu tiên. Đây là đối tác đáng tin cậy.
    [/testimonial]
  [/ux_testimonials]
[/section]
```

**Logo Partners Bar:**
```
[section bg_color="#fff" padding="50px 0" border="bottom" border_color="#eee"]
  [ux_text text_align="center" font_size="13px" text_color="rgba(0,0,0,0.45)" class="partners-label"]
    ĐỐI TÁC & KHÁCH HÀNG TIÊU BIỂU
  [/ux_text]
  [gap height="28px"]
  [ux_logos columns="5" columns__sm="3" gap="large"]
    [ux_logo image="LOGO_ID_1" link="#" opacity="0.5" opacity_hover="1"]
    [ux_logo image="LOGO_ID_2" link="#" opacity="0.5" opacity_hover="1"]
    [ux_logo image="LOGO_ID_3" link="#" opacity="0.5" opacity_hover="1"]
    [ux_logo image="LOGO_ID_4" link="#" opacity="0.5" opacity_hover="1"]
    [ux_logo image="LOGO_ID_5" link="#" opacity="0.5" opacity_hover="1"]
  [/ux_logos]
[/section]
```

---

### 2.8 Pricing Table

**Pricing 3 Gói Chuẩn:**
```
[section padding="80px 0"]
  [title text="Bảng Giá Dịch Vụ" tag="h2" text_align="center"]
  [ux_text text_align="center" text_color="rgba(0,0,0,0.6)"]
    Chọn gói phù hợp — nâng cấp bất cứ lúc nào
  [/ux_text]
  [gap height="48px"]
  [pricing_table]
    [pricing_item
      name="Starter"
      price="990.000"
      currency="₫"
      period="/ tháng"
      features="5 người dùng|10 GB lưu trữ|Hỗ trợ email|Báo cáo cơ bản|API giới hạn"
      btn_text="Bắt Đầu Miễn Phí"
      btn_link="/lien-he/"
    ]
    [pricing_item
      name="Professional"
      price="2.990.000"
      currency="₫"
      period="/ tháng"
      features="Không giới hạn users|100 GB lưu trữ|Hỗ trợ 24/7 ưu tiên|Báo cáo nâng cao|API không giới hạn|Custom domain"
      btn_text="Dùng Thử 14 Ngày"
      btn_link="/lien-he/"
      featured="1"
    ]
    [pricing_item
      name="Enterprise"
      price="Liên Hệ"
      period=""
      features="Tất cả Professional|SLA cam kết 99.9%|Dedicated server|Onboarding 1-1|Custom integration|Hợp đồng dài hạn"
      btn_text="Nhận Báo Giá"
      btn_link="/lien-he/"
    ]
  [/pricing_table]
[/section]
```

---

### 2.9 FAQ & Accordion

```
[section padding="80px 0"]
  [row width="custom" custom_width="820px" h_align="center"]
    [col span="12"]
      [title text="Câu Hỏi Thường Gặp" tag="h2" text_align="center"]
      [gap height="48px"]
      [accordion]
        [accordion_item title="Thời gian hoàn thành dự án mất bao lâu?"]
          Tùy quy mô, thông thường 3–7 ngày làm việc với dự án nhỏ và 2–4 tuần với dự án lớn. Chúng tôi cam kết thông báo tiến độ mỗi ngày và không bao giờ delay mà không báo trước.
        [/accordion_item]
        [accordion_item title="Sau khi bàn giao có hỗ trợ kỹ thuật không?"]
          Có. Bảo hành 12 tháng cho toàn bộ lỗi kỹ thuật. 3 tháng đầu hỗ trợ chỉnh sửa nội dung miễn phí. Sau đó có gói maintenance hàng tháng với mức giá hợp lý.
        [/accordion_item]
        [accordion_item title="Phương thức thanh toán như thế nào?"]
          30% đặt cọc khi ký hợp đồng, 70% khi nghiệm thu hoàn thành. Chấp nhận chuyển khoản ngân hàng, Momo, ZaloPay và thẻ quốc tế.
        [/accordion_item]
        [accordion_item title="Tôi có thể yêu cầu chỉnh sửa thiết kế không?"]
          Tất nhiên. Trong quá trình làm bạn có thể yêu cầu chỉnh sửa không giới hạn lần. Sau bàn giao có 2 lần chỉnh sửa minor miễn phí trong tháng đầu.
        [/accordion_item]
        [accordion_item title="Website có mobile-friendly không?"]
          100%. Mọi website chúng tôi làm đều responsive hoàn toàn, test trên iPhone, Android, tablet và các trình duyệt phổ biến. Đảm bảo điểm PageSpeed Insights trên 90.
        [/accordion_item]
      [/accordion]
    [/col]
  [/row]
[/section]
```

---

### 2.10 Tab Content

```
[tabgroup style="underline" text_align="center"]
  [tab title="🎨 Thiết Kế Web"]
    [row v_align="middle"]
      [col span="6" span__sm="12"]
        [ux_image id="IMAGE_ID" shadow="2" radius="8"]
      [/col]
      [col span="6" span__sm="12" padding="0 0 0 40px" padding__sm="20px 0 0"]
        [ux_text font_size="h3"]Thiết Kế Website Chuyên Nghiệp[/ux_text]
        [ux_text]Giao diện đẹp, tốc độ nhanh, UX tối ưu cho chuyển đổi cao nhất.[/ux_text]
        [button text="Xem Chi Tiết" link="#" radius="5"]
      [/col]
    [/row]
  [/tab]
  [tab title="📱 Mobile App"]
    [row v_align="middle"]
      [col span="6" span__sm="12"]
        [ux_image id="IMAGE_ID_2" shadow="2" radius="8"]
      [/col]
      [col span="6" span__sm="12" padding="0 0 0 40px" padding__sm="20px 0 0"]
        [ux_text font_size="h3"]Ứng Dụng Di Động[/ux_text]
        [ux_text]iOS và Android native hoặc cross-platform với React Native.[/ux_text]
        [button text="Xem Chi Tiết" link="#" radius="5"]
      [/col]
    [/row]
  [/tab]
[/tabgroup]
```

---

### 2.11 Team & About

```
[section padding="80px 0"]
  [title text="Đội Ngũ Chuyên Gia" tag="h2" text_align="center"]
  [gap height="48px"]
  [ux_team columns="4" columns__sm="2" text_align="center" gap="24px"]
    [team name="Nguyễn Văn Anh" role="Giám Đốc Điều Hành" img="IMAGE_ID"
      facebook="#" linkedin="#" twitter="#"]
      10 năm kinh nghiệm, cựu kỹ sư tại Google Singapore.
    [/team]
    [team name="Trần Thị Bình" role="Creative Director" img="IMAGE_ID"
      linkedin="#" instagram="#"]
      Chuyên gia UX/UI, 200+ dự án quốc tế thành công.
    [/team]
    [team name="Lê Hoàng Cường" role="CTO" img="IMAGE_ID"
      linkedin="#" github="#"]
      Full-stack architect, chuyên gia cloud AWS & GCP.
    [/team]
    [team name="Phạm Thu Dung" role="Project Manager" img="IMAGE_ID"
      linkedin="#"]
      PMP certified, quản lý 50+ dự án đồng thời.
    [/team]
  [/ux_team]
[/section]
```

---

### 2.12 Form Liên Hệ & Map

```
[section padding="80px 0"]
  [row]
    [col span="5" span__sm="12"]
      [title text="Liên Hệ Với Chúng Tôi" tag="h2"]
      [gap height="16px"]
      [ux_feature_box pos="left" icon="fas fa-map-marker-alt" icon_color="var(--color-primary)" icon_size="20"]
        123 Đường Nguyễn Huệ, Quận 1, TP.HCM
      [/ux_feature_box]
      [gap height="12px"]
      [ux_feature_box pos="left" icon="fas fa-phone" icon_color="var(--color-primary)" icon_size="20"]
        0901 234 567 (T2–T7, 8:00–17:30)
      [/ux_feature_box]
      [gap height="12px"]
      [ux_feature_box pos="left" icon="fas fa-envelope" icon_color="var(--color-primary)" icon_size="20"]
        info@company.com
      [/ux_feature_box]
      [gap height="24px"]
      [contact-form-7 id="FORM_ID" title="Form Liên Hệ"]
    [/col]
    [col span="7" span__sm="12"]
      [ux_html]
        <iframe
          src="https://maps.google.com/maps?q=Ho+Chi+Minh+City&output=embed"
          width="100%"
          height="500"
          style="border:0;border-radius:12px;display:block;"
          allowfullscreen
          loading="lazy">
        </iframe>
      [/ux_html]
    [/col]
  [/row]
[/section]
```

---

### 2.13 WooCommerce

**Homepage Ecommerce:**
```
[section padding="70px 0"]
  [title text="Sản Phẩm Nổi Bật" tag="h2" text_align="center"]
  [gap height="40px"]
  [products columns="4" columns__sm="2" orderby="popularity" order="DESC" limit="8"]
[/section]

[section padding="40px 0" bg_color="#f8f9fa"]
  [title text="Hàng Mới Về" tag="h2" text_align="center"]
  [gap height="40px"]
  [recent_products limit="4" columns="4" columns__sm="2"]
[/section]

[section padding="70px 0"]
  [title text="Đang Giảm Giá" tag="h2" text_align="center"]
  [gap height="40px"]
  [sale_products limit="4" columns="4" columns__sm="2"]
[/section]
```

**USP Bar WooCommerce:**
```
[section bg_color="#f8f9fa" padding="30px 0" border="top bottom" border_color="#eee"]
  [row h_align="center"]
    [col span="3" span__sm="6" align="center"]
      [ux_feature_box pos="left" icon="fas fa-shipping-fast" icon_color="var(--color-primary)" icon_size="28"]
        [ux_feature_box_title]Freeship Toàn Quốc[/ux_feature_box_title]
        Đơn từ 500k
      [/ux_feature_box]
    [/col]
    [col span="3" span__sm="6" align="center"]
      [ux_feature_box pos="left" icon="fas fa-undo" icon_color="var(--color-primary)" icon_size="28"]
        [ux_feature_box_title]Đổi Trả 30 Ngày[/ux_feature_box_title]
        Không cần lý do
      [/ux_feature_box]
    [/col]
    [col span="3" span__sm="6" align="center"]
      [ux_feature_box pos="left" icon="fas fa-lock" icon_color="var(--color-primary)" icon_size="28"]
        [ux_feature_box_title]Thanh Toán An Toàn[/ux_feature_box_title]
        SSL bảo mật 256-bit
      [/ux_feature_box]
    [/col]
    [col span="3" span__sm="6" align="center"]
      [ux_feature_box pos="left" icon="fas fa-headset" icon_color="var(--color-primary)" icon_size="28"]
        [ux_feature_box_title]Hỗ Trợ 24/7[/ux_feature_box_title]
        Chat, call, email
      [/ux_feature_box]
    [/col]
  [/row]
[/section]
```

---

### 2.14 Global Sections & Block

```bash
# Tạo Global Section (dùng lại ở nhiều trang)
wp post create \
  --post_type=ux_block \
  --post_title="Global — CTA Banner" \
  --post_status=publish \
  --post_content="[section bg_color='var(--color-primary)' text_color='light' padding='60px 0'][row h_align='center'][col span='10' span__sm='12' align='center'][ux_text font_size='h3']Bạn cần tư vấn thêm?[/ux_text][gap height='16px'][button text='Liên Hệ Ngay' link='/lien-he/' size='large' radius='99' style='white'][/col][/row][/section]"

# Lấy ID
BLOCK_ID=$(wp post list --post_type=ux_block --name=global-cta-banner --field=ID)

# Dùng trong trang bất kỳ
# [block id="BLOCK_ID"]
```

### 2.15 Spacing & Utilities

```
[gap height="8px"]
[gap height="40px"]
[gap height="60px" height__sm="30px"]
[divider width="60px" margin="20px auto" color="var(--color-primary)"]
[divider color="rgba(0,0,0,0.08)" margin="0"]
```

---

## ═══ PHẦN 3 — CẤU TRÚC CÁC LOẠI TRANG ═══

### 3.1 Homepage Dịch Vụ / Công Ty

```
1. Hero Banner tĩnh hoặc slider → Headline + CTA chính
2. Logo Bar đối tác/khách hàng
3. Counter: số liệu ấn tượng (4 cột)
4. Features: 3 cột icon top (USP chính)
5. About: 2 cột (ảnh + text + feature list)
6. Services: Tab hoặc 3 cột card
7. Process: 4 bước quy trình
8. Portfolio/Projects: Gallery grid
9. Testimonials: Slider 3 card
10. CTA Bar màu brand
11. Blog: 3 bài mới nhất
12. Footer với contact info
```

### 3.2 Landing Page Chuyển Đổi Cao

```
1. Hero: Headline siêu mạnh + sub + form nhanh / button CTA
2. Social proof bar: số liệu + logo + star rating
3. Problem: Vấn đề khách đang gặp (3 pain points)
4. Solution: Giải pháp của bạn (features + benefits)
5. How it works: 3 bước đơn giản
6. Testimonials: 3 review + video nếu có
7. Pricing: 3 gói với gói giữa featured
8. FAQ: 5-7 câu hỏi phổ biến
9. Final CTA: Urgency + last button
   └── (Không có header/footer đầy đủ — chỉ logo + hotline)
```

### 3.3 Trang Dịch Vụ

```
1. Hero ngắn (400px): Tên dịch vụ + breadcrumb
2. Overview: Mô tả tổng quan (2 cột text + ảnh)
3. Features: Tính năng / lợi ích chi tiết
4. Process: Quy trình 4 bước
5. Cases: Dự án liên quan / portfolio
6. Pricing: Nếu có
7. FAQ: 5 câu hỏi ngành này
8. CTA + Form liên hệ
```

### 3.4 Trang Giới Thiệu

```
1. Hero ngắn: "Về Chúng Tôi" + tagline
2. Story: Câu chuyện thương hiệu (2 cột)
3. Mission/Vision/Values: 3 cột
4. Counter: Thành tựu
5. Team: Grid 4 người
6. Timeline: Lịch sử phát triển
7. Awards/Certs: Logo gallery
8. CTA cuối trang
```

### 3.5 Trang Blog

```
1. Hero ngắn: "Blog / Kiến Thức"
2. [blog_posts columns="3" limit="9" show_category="1" show_date="1"]
3. Pagination
4. Sidebar: Recent posts, categories, search
```

### 3.6 Trang Liên Hệ

```
1. Hero ngắn (300px)
2. Contact info (2 cột: thông tin + form CF7)
3. Google Maps embed
4. FAQ liên hệ ngắn
```

---

## ═══ PHẦN 4 — WP-CLI COMMANDS ═══

### 4.1 Tạo Trang

```bash
# Tạo trang chủ
wp post create \
  --post_type=page \
  --post_title="Trang Chủ" \
  --post_status=publish \
  --post_name="home" \
  --post_content='SHORTCODE_CONTENT_ĐẦY_ĐỦ_Ở_ĐÂY'

# Set làm trang chủ
HOME_ID=$(wp post list --post_type=page --name=home --field=ID)
wp option update show_on_front page
wp option update page_on_front $HOME_ID

# Tạo các trang tiêu chuẩn
for page in "Dich Vu:dich-vu" "Gioi Thieu:gioi-thieu" "Du An:du-an" "Lien He:lien-he" "Bang Gia:bang-gia"; do
  title=$(echo $page | cut -d: -f1)
  slug=$(echo $page | cut -d: -f2)
  wp post create --post_type=page --post_title="$title" --post_status=publish --post_name="$slug" --post_content="[section][row][col][ux_text]Đang cập nhật...[/ux_text][/col][/row][/section]"
done
```

### 4.2 Tạo Menu

```bash
wp menu create "Menu Chính"
MENU_ID=$(wp menu list --field=term_id | head -1)

wp menu item add-post $MENU_ID $(wp post list --post_type=page --name=home --field=ID) --title="Trang Chủ"
wp menu item add-post $MENU_ID $(wp post list --post_type=page --name=dich-vu --field=ID) --title="Dịch Vụ"
wp menu item add-post $MENU_ID $(wp post list --post_type=page --name=du-an --field=ID) --title="Dự Án"
wp menu item add-post $MENU_ID $(wp post list --post_type=page --name=gioi-thieu --field=ID) --title="Giới Thiệu"
wp menu item add-post $MENU_ID $(wp post list --post_type=page --name=lien-he --field=ID) --title="Liên Hệ"

wp menu location assign $MENU_ID primary
wp menu location assign $MENU_ID mobile
```

### 4.3 Upload Media & Lấy ID

```bash
# Upload ảnh từ URL
wp media import "https://example.com/image.jpg" --title="Hero Banner" --porcelain

# List media để lấy ID
wp media list --fields=ID,post_title,post_mime_type --format=table

# Set featured image cho trang
wp post meta update PAGE_ID _thumbnail_id IMAGE_ID
```

### 4.4 CF7 Form

```bash
# Tạo CF7 form liên hệ cơ bản
wp post create \
  --post_type=wpcf7_contact_form \
  --post_title="Form Liên Hệ Chính" \
  --post_status=publish \
  --post_content='<div class="cf7-field">
[text* your-name placeholder "Họ và Tên *"]
[email* your-email placeholder "Email *"]
[tel your-phone placeholder "Số Điện Thoại"]
[textarea your-message placeholder "Nội dung tin nhắn..." rows:5]
[submit "Gửi Tin Nhắn →"]
</div>'

FORM_ID=$(wp post list --post_type=wpcf7_contact_form --field=ID | head -1)
echo "CF7 Form ID: $FORM_ID"
```

### 4.5 Cấu Hình Cuối

```bash
# Flush rewrite rules
wp rewrite flush

# Clear all caches
wp cache flush
wp w3-total-cache flush all 2>/dev/null || true

# Check tất cả trang
wp post list --post_type=page --fields=ID,post_title,post_name,post_status --format=table

# Kiểm tra permalink
wp option get permalink_structure
wp option update permalink_structure "/%postname%/"
wp rewrite flush
```

---

## ═══ PHẦN 5 — CSS MASTER ═══

### 5.1 CSS Toàn Cục (Thêm vào child theme style.css)

```css
/* ============================================
   FLATSOME CHILD — MASTER CSS
   ============================================ */

/* === RESPONSIVE TYPOGRAPHY === */
h1 { font-size: clamp(32px, 5vw, 64px); line-height: 1.1; font-weight: 800; }
h2 { font-size: clamp(26px, 4vw, 48px); line-height: 1.2; font-weight: 700; }
h3 { font-size: clamp(20px, 3vw, 32px); line-height: 1.3; font-weight: 600; }
h4 { font-size: clamp(17px, 2vw, 24px); }

/* === SMOOTH SCROLL === */
html { scroll-behavior: smooth; }

/* === GLOBAL BUTTON === */
.button {
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  font-weight: 600;
  letter-spacing: 0.3px;
}
.button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}

/* === SECTION MOBILE PADDING === */
@media (max-width: 768px) {
  .section { padding-top: 48px !important; padding-bottom: 48px !important; }
}

/* === FEATURE CARD HOVER === */
.feature-card {
  padding: 32px 24px;
  border-radius: 16px;
  transition: all 0.3s ease;
  background: #fff;
  box-shadow: 0 2px 16px rgba(0,0,0,0.06);
}
.feature-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 40px rgba(0,0,0,0.12);
}

/* === CARD UTILITY === */
.card-shadow { box-shadow: 0 2px 20px rgba(0,0,0,0.08); border-radius: 12px; overflow: hidden; }
.card-hover:hover { transform: translateY(-4px); box-shadow: 0 12px 32px rgba(0,0,0,0.12); transition: 0.3s; }

/* === HERO STYLES === */
.hero-label {
  text-transform: uppercase;
  letter-spacing: 2px;
  font-weight: 600;
}
.hero-title { text-shadow: 0 2px 20px rgba(0,0,0,0.3); }

/* === PARTNER LOGOS === */
.partners-label { text-transform: uppercase; letter-spacing: 2px; }

/* === SECTION DIVIDER WAVE === */
.section-wave { position: relative; }
.section-wave::after {
  content: '';
  position: absolute;
  bottom: -1px; left: 0; right: 0;
  height: 70px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1440 70'%3E%3Cpath fill='%23f8f9fa' d='M0,40L48,45C96,50,192,60,288,58C384,56,480,40,576,36C672,32,768,40,864,44C960,48,1056,48,1152,44C1248,40,1344,32,1392,28L1440,24L1440,70L1392,70C1344,70,1248,70,1152,70C1056,70,960,70,864,70C768,70,672,70,576,70C480,70,384,70,288,70C192,70,96,70,48,70L0,70Z'/%3E%3C/svg%3E");
  background-size: cover;
  background-repeat: no-repeat;
}

/* === LAZY IMAGE FADEIN === */
.ux-lazy-loaded { animation: fadeInUp 0.6s ease forwards; }
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* === STICKY HEADER SHADOW === */
.header--sticky.stuck { box-shadow: 0 2px 24px rgba(0,0,0,0.1); }

/* === EYEBROW LABEL === */
.eyebrow-label {
  text-transform: uppercase;
  letter-spacing: 2px;
  font-weight: 700;
  font-size: 13px;
}
```

### 5.2 CSS Landing Page

```css
/* === LANDING PAGE === */
.urgency-badge {
  display: inline-block;
  background: #e74c3c;
  color: #fff;
  padding: 5px 14px;
  border-radius: 99px;
  font-size: 13px;
  font-weight: 700;
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.trust-bar { border-top: 1px solid rgba(0,0,0,0.08); padding-top: 20px; }
.countdown-timer { font-size: 48px; font-weight: 800; color: var(--color-primary); }
```

### 5.3 CSS WooCommerce

```css
/* === WOOCOMMERCE === */
.product-small:hover { transform: translateY(-4px); transition: 0.3s ease; }
.onsale {
  background: var(--color-primary) !important;
  border-radius: 6px !important;
  font-weight: 700 !important;
}
.add_to_cart_button { border-radius: 99px !important; font-weight: 600 !important; }
.woocommerce-loop-product__title { font-size: 15px !important; font-weight: 600 !important; }

/* Product card */
.product-small .box {
  border-radius: 12px !important;
  overflow: hidden !important;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
  transition: box-shadow 0.3s ease;
}
.product-small:hover .box { box-shadow: 0 8px 32px rgba(0,0,0,0.12) !important; }
```

### 5.4 CSS CTA Gradient (Linh Hoạt)

```css
/* Gradient tím xanh */
.cta-purple { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }

/* Gradient cam vàng */
.cta-orange { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }

/* Gradient xanh lá */
.cta-green { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }

/* Dark gradient */
.cta-dark { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); }
```

---

## ═══ PHẦN 6 — HEADER & FOOTER ═══

### 6.1 Header Configurations

**Website Dịch Vụ (Logo Trái + Menu Phải + Button):**
```
Flatsome > Header > Row 1:
  Left:   Logo
  Center: (trống)
  Right:  Nav Menu [primary] | Button "Liên Hệ Ngay" [link=/lien-he/]

Sticky: Row 1
Transparent on hero: ON
```

**WooCommerce (Logo + Search + Cart):**
```
Flatsome > Header > Row 1:
  Left:   Logo
  Center: Search Bar
  Right:  Wishlist | Cart Icon | Account Icon

Row 2:
  Center: Nav Menu [primary]

Sticky: Row 1
```

**Minimalist (Logo Giữa + Menu Dưới):**
```
Flatsome > Header > Row 1:
  Center: Logo

Row 2:
  Center: Nav Menu [primary]
```

### 6.2 Footer WP-CLI

```bash
# Widget text giới thiệu (Footer Area 1)
wp widget add text flatsome-footer-1 1 \
  --title="Về Chúng Tôi" \
  --text="<p>Công ty chuyên cung cấp giải pháp công nghệ tối ưu, uy tín hơn 10 năm trên thị trường.</p>" \
  --filter=true

# Widget menu nhanh (Footer Area 2)
wp menu create "Footer Menu"
FOOTER_MENU=$(wp menu list --field=term_id | tail -1)
wp menu location assign $FOOTER_MENU footer
wp widget add nav_menu flatsome-footer-2 1 \
  --nav_menu=$FOOTER_MENU \
  --title="Liên Kết Nhanh"

# Footer copyright
wp option patch update flatsome_options footer_copyright \
  "© 2026 Tên Công Ty. Bảo lưu mọi quyền. | <a href='/chinh-sach-bao-mat/'>Chính Sách</a> | <a href='/dieu-khoan/'>Điều Khoản</a>"
```

---

## ═══ PHẦN 7 — CLONE TỪ MẪU ═══

### 7.1 Quy Trình Phân Tích Ảnh Mẫu

Khi nhận ảnh/screenshot, AI thực hiện:

```
BƯỚC 1 — ĐỌC CẤU TRÚC
  □ Đếm sections từ top xuống bottom
  □ Xác định màu nền mỗi section
  □ Xác định layout: 1 cột / 2 cột / 3 cột / 4 cột / full-width

BƯỚC 2 — XÁC ĐỊNH COMPONENTS
  □ Hero: banner tĩnh / slider / split / video
  □ Features: icon top / icon left / card grid
  □ Testimonials: slider / grid / quote
  □ Pricing: 2/3/4 cột, featured highlight
  □ CTA: inline / full-width bar / popup
  □ Form: sidebar / standalone / popup
  □ Media: gallery / carousel / lightbox

BƯỚC 3 — MÀU SẮC & TYPOGRAPHY
  □ Primary color (màu nút, icon, accent)
  □ Background colors từng section
  □ Heading font size tương đối
  □ Body text color

BƯỚC 4 — MAPPING SHORTCODE
  □ Mỗi section → [section bg_color="" padding=""]
  □ Mỗi layout → [row] [col span=""]
  □ Mỗi element → shortcode tương ứng

BƯỚC 5 — OUTPUT
  □ Full shortcode sẵn paste vào WP
  □ CSS bổ sung nếu cần
  □ Note: IMAGE_ID, FORM_ID cần thay thế
```

### 7.2 Mapping Visual → Shortcode

| Nhìn thấy trong mẫu | Shortcode dùng |
|---------------------|----------------|
| Ảnh fullscreen + text overlay | `[ux_banner]` + `[text_box]` |
| Slider nhiều ảnh | `[ux_slider]` + `[ux_banner]` |
| Grid 3 cột với icon | `[row]` + `[col span="4"]` + `[ux_feature_box]` |
| Card review với ảnh avatar | `[ux_testimonials]` + `[testimonial]` |
| 3 box giá tiền | `[pricing_table]` + `[pricing_item]` |
| Accordion mở/đóng | `[accordion]` + `[accordion_item]` |
| Tab ngang | `[tabgroup]` + `[tab]` |
| Số đếm animated | `[ux_counter]` |
| Logo dãy ngang | `[ux_logos]` + `[ux_logo]` |
| Ảnh lưới + lightbox | `[ux_gallery]` + `[ux_gallery_item]` |
| Video embed | `[ux_video]` |
| Form liên hệ | `[contact-form-7 id=""]` |
| Bản đồ Google | `[ux_html]` với iframe |
| Team cards | `[ux_team]` + `[team]` |
| Blog posts | `[blog_posts]` |
| Sản phẩm WP | `[products]` |
| Thanh phân cách | `[divider]` |
| Khoảng trắng | `[gap height=""]` |
| Button | `[button]` |

---

## ═══ PHẦN 8 — XỬ LÝ LỖI ═══

### 8.1 Lỗi Thường Gặp

| Triệu chứng | Nguyên nhân | Giải pháp |
|-------------|-------------|-----------|
| Trang trắng trắng | Shortcode không đóng tag | Kiểm tra `[/section]` `[/row]` `[/col]` |
| Shortcode hiện dạng text | Plugin Flatsome/UXBuilder chưa active | `wp plugin activate flatsome` |
| Menu không hiện trên site | Sai menu location | `wp menu location list` → assign đúng |
| CSS không áp dụng | Child theme chưa active | `wp theme activate flatsome-child` |
| WP-CLI lỗi "wp not found" | Thiếu PATH LocalWP | Set `WP_CLI_PHP` export |
| Ảnh không load | IMAGE_ID sai | `wp media list --fields=ID,post_title` |
| Form CF7 không gửi | Form ID sai | `wp post list --post_type=wpcf7_contact_form` |
| Layout vỡ mobile | Thiếu `span__sm="12"` | Thêm vào tất cả `[col]` |
| Màu không đúng | Dùng sai CSS variable | Kiểm tra `--color-primary` trong Flatsome > Theme Options |

### 8.2 Debug Commands

```bash
# Xem content trang
wp post get PAGE_ID --field=post_content

# Tìm trang theo tên
wp post list --post_type=page --search="keyword" --fields=ID,post_title,post_status

# Kiểm tra plugin
wp plugin list --status=active --fields=name,version --format=table

# Flush cache
wp rewrite flush && wp cache flush

# Xóa trang để làm lại
wp post delete PAGE_ID --force

# Check site URL
wp option get siteurl && wp option get home
```

---

## ═══ PHẦN 9 — CHECKLIST BÀN GIAO ═══

```
KỸ THUẬT:
  □ Child theme active, không sửa theme gốc
  □ Tất cả trang published, slug đúng (tiếng Việt không dấu)
  □ Menu primary, mobile, footer đã assign
  □ Trang chủ đã set (show_on_front = page)
  □ Rewrite rules đã flush
  □ Cache đã clear
  □ WP Debug tắt (production)

THIẾT KẾ:
  □ 100% dùng shortcode UXBuilder (không HTML thô)
  □ Responsive: 320px / 768px / 1280px / 1440px ✓
  □ CTA rõ ràng đầu và cuối mỗi trang chính
  □ Màu brand nhất quán toàn site
  □ Typography nhất quán
  □ Ảnh đã upload (không dùng URL ngoài)
  □ Không còn placeholder: "IMAGE_ID", "FORM_ID", "Lorem ipsum"

NỘI DUNG:
  □ Tiêu đề, mô tả phù hợp ngành nghề
  □ Thông tin liên hệ đúng (SĐT, email, địa chỉ)
  □ Form CF7 gửi được + nhận mail
  □ Internal links không 404
  □ SEO: title, meta description từng trang

BÁO CÁO CUỐI:
  URL trang chủ: [siteurl]
  Danh sách trang đã tạo + URL slug
  Hướng dẫn đăng nhập admin
  Hướng dẫn chỉnh sửa nội dung qua UXBuilder
  Lưu ý: IMAGE_ID cần thay bằng ID ảnh thật sau khi upload
```

---

## ═══ PHẦN 10 — MAPPING NHANH ═══

| Người dùng nói / gửi mẫu có | AI làm gì |
|------------------------------|-----------|
| Ảnh hero fullscreen + text | `[ux_banner]` + `[text_box]` |
| "Trang chủ dịch vụ" | Phần 3.1 — 12 sections đầy đủ |
| "Landing page bán hàng" | Phần 3.2 — 9 sections chuyển đổi cao |
| "Trang dịch vụ" | Phần 3.3 — 8 sections |
| "Trang giới thiệu" | Phần 3.4 — 8 sections |
| "Trang liên hệ" | Form + map + FAQ |
| "Thêm section review" | `[ux_testimonials]` slider |
| "Bảng giá 3 gói" | `[pricing_table]` 3 items |
| "FAQ" | `[accordion]` 5-7 items |
| "Danh sách sản phẩm WP" | `[products columns="4"]` |
| "Gallery portfolio" | `[ux_gallery type="masonry"]` |
| "Đổi màu primary" | `wp option patch update flatsome_options color_primary` |
| "Thêm menu item" | `wp menu item add-post` |
| "Clone trang" | `wp post get --field=post_content` → `wp post create` |
| "Header trong suốt" | Flatsome > Header > Transparent = ON |
| "Footer 4 cột" | 4 widget areas + copyright |

---

*SKILL VERSION: 2.0 — Flatsome Master Builder*
*Tối ưu cho: Clone từ mẫu 100% | UXBuilder Shortcode | CSS thuần | WP-CLI*
