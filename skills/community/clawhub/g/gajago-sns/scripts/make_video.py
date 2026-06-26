from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os, subprocess, shutil

INBOUND = "/Users/isangsu/.openclaw/media/inbound"
OUTBOUND = "/Users/isangsu/.openclaw/media/outbound"
TMP = "/tmp/gajago_frames_v3"
os.makedirs(TMP, exist_ok=True)

W, H = 1080, 1080
FPS = 30
DURATION_PER = 4
TOTAL = 20
FADE_FRAMES = 18  # 0.6초

photos = [
    f"{INBOUND}/KakaoTalk_Photo_2026-03-26-21-10-48_001---331e24a3-2f7c-475b-b268-c6ca495f550c.jpg",
    f"{INBOUND}/KakaoTalk_Photo_2026-03-26-21-10-49_002---abf104e5-7dc0-4ce0-be06-e3ad20e76aff.jpg",
    f"{INBOUND}/KakaoTalk_Photo_2026-03-26-21-10-50_003---3162ad30-b799-4654-bc92-1f05b7b50240.jpg",
    f"{INBOUND}/KakaoTalk_Photo_2026-03-26-21-10-51_004---f6e07577-6c82-404e-b2ab-aa8adcc8d81c.jpg",
    f"{INBOUND}/KakaoTalk_Photo_2026-03-26-21-10-52_005---dab99a9a-fde9-4693-8a45-6128b93373be.jpg",
]

scenes = [
    {"badge": "업무협약 체결", "title": "경기도교육청 취창업지원센터", "sub": "× 한국인공지능소프트웨어산업협회", "date": "2026. 3. 25"},
    {"badge": "전국 최초", "title": "17개 시도교육청 중 최초", "sub": "AI 관련 업무협약 체결", "date": ""},
    {"badge": "현장실습 · 취업연계", "title": "직업계고 학생들의", "sub": "AI · SW 미래를 열다", "date": ""},
    {"badge": "2026 하반기 운영", "title": "AI · 로보틱스 미래인재", "sub": "양성 아카데미 출범", "date": "1만5천 회원사 네트워크 활용"},
    {"badge": "GAJAGO", "title": "경기도교육청", "sub": "취창업지원센터가 함께합니다", "date": "김혜리 진로직업교육과장 추진"},
]

try:
    font_big   = ImageFont.truetype("/System/Library/Fonts/Supplemental/AppleGothic.ttf", 50)
    font_sub   = ImageFont.truetype("/System/Library/Fonts/Supplemental/AppleGothic.ttf", 26)
    font_badge = ImageFont.truetype("/System/Library/Fonts/Supplemental/AppleGothic.ttf", 18)
    font_date  = ImageFont.truetype("/System/Library/Fonts/Supplemental/AppleGothic.ttf", 20)
except:
    font_big = font_sub = font_badge = font_date = ImageFont.load_default()

CORAL = (255, 87, 51)
NAVY  = (26, 46, 90)
WHITE = (255, 255, 255)
LGRAY = (200, 200, 200)

def crop_center(img, w, h):
    iw, ih = img.size
    scale = max(w/iw, h/ih)
    nw, nh = int(iw*scale), int(ih*scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - w) // 2
    top  = (nh - h) // 2
    return img.crop((left, top, left+w, top+h))

def ken_burns(img, frame, total_frames, w, h):
    t = frame / total_frames
    zoom = 1.0 + 0.07 * t
    nw = int(w * zoom)
    nh = int(h * zoom)
    img_big = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - w) // 2
    top  = (nh - h) // 2
    return img_big.crop((left, top, left+w, top+h))

def draw_overlay(base, scene, alpha):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    la = int(255 * alpha)

    # ── 하단 그라데이션 (하단 30%만, 더 집중적으로) ──
    grad_start = int(H * 0.70)  # 70%부터 시작 (기존 50%에서 내림)
    for y in range(grad_start, H):
        t = (y - grad_start) / (H - grad_start)
        a = int(min(210, t * 240) * alpha)
        draw.line([(0, y), (W, y)], fill=(*NAVY, a))

    # ── 텍스트 시작 Y 위치 (하단 기준으로 배치) ──
    # 전체 텍스트 블록 높이 계산 후 하단 정렬
    has_date = bool(scene.get("date"))
    block_h = 32 + 12 + 58 + 36 + (36 if has_date else 0)  # badge+gap+title+sub+date
    bottom_margin = 52
    block_y = H - bottom_margin - block_h  # 하단에서 block_h만큼 위

    # ── 코랄 강조선 ──
    line_x2 = 100
    draw.rectangle([40, block_y - 14, line_x2, block_y - 11], fill=(*CORAL, la))

    # ── 배지 ──
    badge = scene["badge"]
    bx, by = 40, block_y
    bbox = draw.textbbox((bx, by), badge, font=font_badge)
    pw = bbox[2] - bbox[0] + 22
    ph = bbox[3] - bbox[1] + 10
    draw.rounded_rectangle([bx, by, bx+pw, by+ph], radius=5, fill=(*CORAL, int(230*alpha)))
    draw.text((bx+11, by+5), badge, font=font_badge, fill=(*WHITE, la))

    # ── 메인 타이틀 ──
    ty = by + ph + 10
    draw.text((40, ty), scene["title"], font=font_big, fill=(*WHITE, la))

    # ── 서브타이틀 ──
    sy = ty + 58
    draw.text((40, sy), scene["sub"], font=font_sub, fill=(*LGRAY, int(210*alpha)))

    # ── 날짜 ──
    if has_date:
        dy = sy + 36
        draw.text((40, dy), scene["date"], font=font_date, fill=(*LGRAY, int(170*alpha)))

    return Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGB")


print("📸 사진 로딩 중...")
imgs = []
for p in photos:
    img = Image.open(p)
    img = crop_center(img, W, H)
    img = ImageEnhance.Contrast(img).enhance(1.1)
    imgs.append(img)

total_frames = TOTAL * FPS
print(f"🎬 총 {total_frames}프레임 생성 중...")

for scene_idx, (img, scene) in enumerate(zip(imgs, scenes)):
    scene_frames = DURATION_PER * FPS
    for f in range(scene_frames):
        global_f = scene_idx * scene_frames + f
        frame_img = ken_burns(img, f, scene_frames, W, H)

        if f < FADE_FRAMES:
            text_alpha = f / FADE_FRAMES
        elif f > scene_frames - FADE_FRAMES:
            text_alpha = (scene_frames - f) / FADE_FRAMES
        else:
            text_alpha = 1.0

        final = draw_overlay(frame_img, scene, text_alpha)
        fname = f"{TMP}/frame_{global_f:05d}.jpg"
        final.save(fname, "JPEG", quality=92)

        if global_f % 60 == 0:
            print(f"  {global_f}/{total_frames} ({global_f/total_frames*100:.0f}%)")

# BGM 선택 (더 밝고 신나는 버전 우선)
bgm = "/tmp/gajago-bgm-new.mp3"
if not os.path.exists(bgm) or os.path.getsize(bgm) < 100000:
    bgm = "/tmp/gajago-bgm-v2.mp3"
if not os.path.exists(bgm) or os.path.getsize(bgm) < 100000:
    bgm = "/tmp/gajago-bgm.mp3"
print(f"\n🎵 BGM: {bgm}")

output = f"{OUTBOUND}/2026-03-27-gajago-mou-v2.mp4"
cmd = [
    "ffmpeg", "-y",
    "-framerate", str(FPS),
    "-i", f"{TMP}/frame_%05d.jpg",
    "-i", bgm,
    "-map", "0:v", "-map", "1:a",
    "-c:v", "libx264", "-crf", "17", "-preset", "fast",
    "-c:a", "aac", "-b:a", "192k",
    "-af", f"afade=t=in:st=0:d=1,afade=t=out:st=18:d=2,volume=0.75",
    "-t", str(TOTAL),
    "-pix_fmt", "yuv420p",
    "-movflags", "+faststart",
    output
]
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode == 0:
    size = os.path.getsize(output) / 1024 / 1024
    print(f"\n✅ 완성! {output} ({size:.1f} MB)")
    shutil.rmtree(TMP)
else:
    print(f"오류: {r.stderr[-400:]}")
