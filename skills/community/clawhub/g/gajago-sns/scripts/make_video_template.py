from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os, subprocess, shutil

INBOUND = "/Users/isangsu/.openclaw/media/inbound"
OUTBOUND = "/Users/isangsu/.openclaw/media/outbound"
TMP = "/tmp/gajago_frames"
os.makedirs(TMP, exist_ok=True)

W, H = 1080, 1080
FPS = 30
DURATION_PER = 4  # 4초씩
TOTAL = 20
FADE_FRAMES = 15  # 0.5초 페이드

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

# 폰트 - 시스템 폰트 사용
try:
    font_bold = ImageFont.truetype("/System/Library/Fonts/Supplemental/AppleGothic.ttf", 42)
    font_sub  = ImageFont.truetype("/System/Library/Fonts/Supplemental/AppleGothic.ttf", 26)
    font_badge= ImageFont.truetype("/System/Library/Fonts/Supplemental/AppleGothic.ttf", 18)
    font_date = ImageFont.truetype("/System/Library/Fonts/Supplemental/AppleGothic.ttf", 20)
    font_big  = ImageFont.truetype("/System/Library/Fonts/Supplemental/AppleGothic.ttf", 52)
except:
    font_bold = font_sub = font_badge = font_date = font_big = ImageFont.load_default()

CORAL = (255, 87, 51)
NAVY  = (26, 46, 90)
WHITE = (255, 255, 255)
LGRAY = (200, 200, 200)
LIME  = (109, 204, 90)

def crop_center(img, w, h):
    iw, ih = img.size
    scale = max(w/iw, h/ih)
    nw, nh = int(iw*scale), int(ih*scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - w) // 2
    top  = (nh - h) // 2
    return img.crop((left, top, left+w, top+h))

def ken_burns(img, frame, total_frames, w, h):
    """줌인 효과: 1.0 → 1.08"""
    t = frame / total_frames
    zoom = 1.0 + 0.08 * t
    nw = int(w * zoom)
    nh = int(h * zoom)
    img_big = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - w) // 2
    top  = (nh - h) // 2
    return img_big.crop((left, top, left+w, top+h))

def draw_overlay(base, scene, alpha):
    """세련된 텍스트 오버레이"""
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    
    # 하단 그라데이션 (반투명 네이비)
    for y in range(H//2, H):
        t = (y - H//2) / (H//2)
        a = int(min(200, t * 220) * alpha)
        draw.line([(0, y), (W, y)], fill=(26, 46, 90, a))
    
    # 코랄 구분선
    line_y = int(H * 0.56)
    la = int(255 * alpha)
    draw.rectangle([40, line_y, 120, line_y+3], fill=(*CORAL, la))
    
    # 배지
    badge = scene["badge"]
    bx, by = 40, line_y + 14
    bbox = draw.textbbox((bx, by), badge, font=font_badge)
    pw, ph = bbox[2]-bbox[0]+20, bbox[3]-bbox[1]+10
    ba = int(230 * alpha)
    draw.rounded_rectangle([bx, by, bx+pw, by+ph], radius=4, fill=(*CORAL, ba))
    draw.text((bx+10, by+5), badge, font=font_badge, fill=(*WHITE, la))
    
    # 메인 타이틀
    ty = by + ph + 18
    draw.text((40, ty), scene["title"], font=font_big, fill=(*WHITE, la))
    
    # 서브타이틀
    sy = ty + 62
    draw.text((40, sy), scene["sub"], font=font_sub, fill=(*LGRAY, int(200*alpha)))
    
    # 날짜
    if scene.get("date"):
        dy = sy + 40
        draw.text((40, dy), scene["date"], font=font_date, fill=(*LGRAY, int(160*alpha)))
    
    return Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGB")

frame_idx = 0
total_frames = TOTAL * FPS

print("📸 사진 로딩 중...")
imgs = []
for p in photos:
    img = Image.open(p)
    img = crop_center(img, W, H)
    # 약간 대비 강화
    img = ImageEnhance.Contrast(img).enhance(1.1)
    imgs.append(img)

print(f"🎬 총 {total_frames}프레임 생성 중...")

for scene_idx, (img, scene) in enumerate(zip(imgs, scenes)):
    scene_frames = DURATION_PER * FPS
    for f in range(scene_frames):
        global_f = scene_idx * scene_frames + f
        
        # Ken Burns
        frame_img = ken_burns(img, f, scene_frames, W, H)
        
        # 텍스트 알파 (페이드인/아웃)
        if f < FADE_FRAMES:
            text_alpha = f / FADE_FRAMES
        elif f > scene_frames - FADE_FRAMES:
            text_alpha = (scene_frames - f) / FADE_FRAMES
        else:
            text_alpha = 1.0
        
        # 오버레이
        final = draw_overlay(frame_img, scene, text_alpha)
        
        # 저장
        fname = f"{TMP}/frame_{global_f:05d}.jpg"
        final.save(fname, "JPEG", quality=92)
        
        if global_f % 60 == 0:
            print(f"  프레임 {global_f}/{total_frames} ({global_f/total_frames*100:.0f}%)")

print("\n🎵 영상 인코딩 + 음악 합성...")
output = f"{OUTBOUND}/2026-03-27-gajago-mou-video.mp4"
cmd = [
    "ffmpeg", "-y",
    "-framerate", str(FPS),
    "-i", f"{TMP}/frame_%05d.jpg",
    "-i", "/tmp/gajago-bgm.mp3",
    "-map", "0:v", "-map", "1:a",
    "-c:v", "libx264", "-crf", "18", "-preset", "fast",
    "-c:a", "aac", "-b:a", "192k",
    "-af", f"afade=t=in:st=0:d=1.5,afade=t=out:st=17.5:d=2.5,volume=0.65",
    "-t", str(TOTAL),
    "-pix_fmt", "yuv420p",
    "-movflags", "+faststart",
    output
]
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode == 0:
    size = os.path.getsize(output)/1024/1024
    print(f"\n✅ 완성! {output} ({size:.1f} MB)")
    shutil.rmtree(TMP)
else:
    print(f"오류: {r.stderr[-400:]}")

