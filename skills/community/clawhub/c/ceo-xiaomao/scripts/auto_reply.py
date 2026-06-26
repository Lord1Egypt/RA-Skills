#!/usr/bin/env python3
"""
WhatsApp 全自动跟单增强版
功能：
1. 📩 文字消息 → AI 会话助理（支持15+语言）
2. 🖼️ 客户发图片 → AI 识别图片内容并回复
3. 📄 发送产品图册 PDF
4. 🖼️ 发送产品图片
5. 🎬 发送产品视频
6. 🚨 意向记录 → 通知老板
7. 🔍 自动发现新联系人 → 主动监听起来

配置：
- WhatsApp service: GREEN_API_URL / GREEN_API_INSTANCE_ID / GREEN_API_CREDENTIAL
- AI agent: OPENCLAW_AGENT (default: sales_agent)
- 工作目录: XIAONENG_DIR (default: .)
- Optional scheduler can relaunch the assistant if needed
"""

import json, os, time, requests, subprocess, shutil, re
from datetime import datetime

# ============== 环境变量配置 ==============
API_URL   = os.environ.get('GREEN_API_URL',         'https://7107.api.greenapi.com')
INSTANCE_ID = os.environ.get('GREEN_API_INSTANCE_ID', '')
SERVICE_CREDENTIAL = os.environ.get('GREEN_API_CREDENTIAL') or os.environ.get('SERVICE_CREDENTIAL', '')
WORK_DIR    = os.environ.get('XIAONENG_DIR',         os.path.dirname(os.path.abspath(__file__)))
AI_AGENT    = os.environ.get('OPENCLAW_AGENT',       'sales_agent')

if not INSTANCE_ID or not SERVICE_CREDENTIAL:
    raise SystemExit('Missing GREEN_API_INSTANCE_ID / GREEN_API_CREDENTIAL')

STATE_FILE = os.path.join(WORK_DIR, '.auto_state_v3.json')
LOG_FILE   = os.path.join(WORK_DIR, 'auto_reply.log')
CUSTOMERS_FILE = os.path.join(WORK_DIR, '.known_customers.json')
NOTIFY_FILE    = os.path.join(WORK_DIR, '.boss_notifications.json')
PRODUCT_DB_FILE = os.path.join(WORK_DIR, '.product_db.json')

MIN_REPEAT_WAIT = 45
HIGH_INTENT = ['quote','price','sample','catalog','interested','order','MOQ','payment',
               'delivery','spec','1000','500','2000','批发','报价','样品','目录','我要']

# ============== 产品资料库（可由 .product_db.json 覆盖）==============
DEFAULT_PRODUCT_FILES = {}
DEFAULT_PRODUCT_IMAGES = {}
DEFAULT_PRODUCT_VIDEOS = {}

DEFAULT_PRODUCT_INFO = (
    "Product: [请在 .product_db.json 中配置产品名称]\n"
    "Features: [请在 .product_db.json 中配置产品特性]\n"
    "MOQ: [请在 .product_db.json 中配置起订量]\n"
    "Terms: FOB / CIF / EXW available\n"
)

def load_product_db():
    if os.path.exists(PRODUCT_DB_FILE):
        try:
            return json.load(open(PRODUCT_DB_FILE))
        except Exception:
            pass
    return {
        'product_name': '[Product Name]',
        'product_info': DEFAULT_PRODUCT_INFO,
        'catalog': [],
        'images': [],
        'videos': [],
        'fallback_image_url': '',
    }

PRODUCT_DB = load_product_db()

def get_product_files():
    return PRODUCT_DB.get('catalog', DEFAULT_PRODUCT_FILES)

def get_product_images():
    imgs = PRODUCT_DB.get('images', DEFAULT_PRODUCT_IMAGES)
    if imgs:
        return {f'img_{i}': v for i, v in enumerate(imgs)}
    fallback_url = PRODUCT_DB.get('fallback_image_url', '')
    if fallback_url:
        return {'fallback': {'url': fallback_url, 'caption': 'Product photo 🚿', 'type': 'image'}}
    return {}

def get_product_videos():
    return {v.get('key', f'vid_{i}'): v for i, v in enumerate(PRODUCT_DB.get('videos', DEFAULT_PRODUCT_VIDEOS))}

PRODUCT_FILES  = get_product_files()
PRODUCT_IMAGES = get_product_images()
PRODUCT_VIDEOS = get_product_videos()
PRODUCT_INFO   = PRODUCT_DB.get('product_info', DEFAULT_PRODUCT_INFO)


# ============== 工具函数 ==============

def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{ts}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(line + '\n')
    except Exception:
        pass

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            state = json.load(f)
    else:
        state = {'baseline': {}, 'replied_at': {}, 'lang_profile': {}}
    state.setdefault('baseline', {})
    state.setdefault('replied_at', {})
    state.setdefault('lang_profile', {})
    return state

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def api(url, method='POST', json_data=None):
    try:
        if method == 'GET':
            r = requests.get(url, timeout=15)
        else:
            r = requests.post(url, json=json_data, timeout=20)
        if r.status_code == 200 and r.text.strip():
            return r.json()
    except Exception as e:
        log(f"⚠️ API 请求异常: {e}")
    return []

def send_text(phone, text):
    url = f"{API_URL}/waInstance{INSTANCE_ID}/sendMessage/{SERVICE_CREDENTIAL}"
    r = api(url, json_data={"chatId": f"{phone}@c.us", "message": text})
    if 'idMessage' in r:
        log(f"📤 文字回复 {phone}: {text[:50]}")
        return True, r['idMessage']
    log(f"❌ 文字发送失败 {phone}: {r}")
    return False, r

def send_file_by_upload(phone, file_path, caption, file_name=None):
    if not os.path.exists(file_path):
        log(f"❌ 文件不存在: {file_path}")
        return False, "file not found"
    ext = os.path.splitext(file_name or file_path)[1].lower()
    mime = {'.pdf':'application/pdf','.jpg':'image/jpeg','.jpeg':'image/jpeg',
            '.png':'image/png','.mp4':'video/mp4'}.get(ext, 'application/octet-stream')
    try:
        with open(file_path, 'rb') as f:
            files = {'file': ((file_name or os.path.basename(file_path)), f, mime)}
            data = {'chatId': f"{phone}@c.us", 'caption': caption}
            r = requests.post(
                f"{API_URL}/waInstance{INSTANCE_ID}/sendFileByUpload/{SERVICE_CREDENTIAL}",
                data=data, files=files, timeout=120
            )
        result = r.json()
        if 'idMessage' in result:
            log(f"📎 文件已发送 {phone}: {os.path.basename(file_path)} → {result['idMessage']}")
            return True, result['idMessage']
        log(f"❌ 文件发送失败: {result}")
        return False, result
    except Exception as e:
        log(f"❌ 文件上传异常: {e}")
        return False, str(e)

def send_file_by_url(phone, url, file_name, caption):
    r = api(
        f"{API_URL}/waInstance{INSTANCE_ID}/sendFileByUrl/{SERVICE_CREDENTIAL}",
        json_data={"chatId": f"{phone}@c.us", "urlFile": url, "fileName": file_name, "caption": caption}
    )
    if 'idMessage' in r:
        log(f"🌐 URL文件已发送 {phone}: {file_name}")
        return True, r['idMessage']
    log(f"❌ URL文件发送失败: {r}")
    return False, r

def download_file(url, save_path):
    try:
        r = requests.get(url, timeout=60, stream=True)
        if r.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in r.iter_content(8192): f.write(chunk)
            return save_path
    except Exception as e:
        log(f"⚠️ 下载失败: {e}")
    return None

def ai_analyze_image(image_path, context=""):
    prompt = (
        f"You are a professional B2B sales rep. A customer sent an image.\n"
        f"{context}\n"
        f"Image: {image_path}\n\n"
        f"Please describe the image, infer the customer's intent, and reply in English (1-3 sentences). Output ONLY the reply text."
    )
    try:
        openclaw_bin = shutil.which('openclaw')
        result = subprocess.run(
            [openclaw_bin, 'agent', '--agent', AI_AGENT,
             '--message', prompt, '--timeout', '40'],
            capture_output=True, text=True, timeout=50
        )
        for line in result.stdout.strip().split('\n'):
            line = line.strip()
            if line and not line.startswith('[plugins]') and not line.startswith('🦞'):
                return line
    except Exception as e:
        log(f"⚠️ AI图片分析异常: {e}")
    return "Thanks for sharing! We've received your image and will check it right away. 🚿"

def ai_generate_reply(prompt_text):
    try:
        openclaw_bin = shutil.which('openclaw')
        result = subprocess.run(
            [openclaw_bin, 'agent', '--agent', AI_AGENT,
             '--message', prompt_text, '--timeout', '25'],
            capture_output=True, text=True, timeout=35
        )
        for line in result.stdout.strip().split('\n'):
            line = line.strip()
            if line and not line.startswith('[plugins]') and not line.startswith('🦞'):
                return line
    except Exception as e:
        log(f"⚠️ AI回复生成异常: {e}")
    return None


# ============== 语言检测 ==============

LANG_MAP = {
    'ja': ('日语', '日本語で返事してください。プロフェッショナルで親しみやすく、3文以内で、具体的な価格は避けてください。'),
    'zh': ('中文', '请用中文回复。专业友好，简洁，不超过3句，不承诺具体价格。'),
    'ko': ('韩语', '한국어로 답변해 주세요。専門적이면서 친절하게、3문장 이내로、구체적인 가격은 언급하지 마세요。'),
    'ar': ('阿拉伯语', 'رد بالعربية. احترافي وودود، موجز، 3 جمل كحد أقصى. لا تذكر أسعارًا محددة.'),
    'ru': ('俄语', 'Отвечайте на русском. Профессионально, дружелюбно, кратко, до 3 предложений.'),
    'th': ('泰语', 'ตอบเป็นภาษาไทย แบบมืออาชีพ เป็นมิตร กระชับ ไม่เกิน 3 ประโยค และไม่ระบุราคาเฉพาะเจาะจง'),
    'vi': ('越南语', 'Trả lời bằng tiếng Việt. Chuyên nghiệp, thân thiện, ngắn gọn, tối đa 3 câu. Không báo giá cụ thể.'),
    'es': ('西班牙语', 'Responde en español. Profesional, amable, conciso, máximo 3 oraciones. No menciones precios específicos.'),
    'pt': ('葡萄牙语', 'Responda em português. Profissional, amigável, conciso, máximo 3 frases. Não cite preços específicos.'),
    'de': ('德语', 'Antworten Sie auf Deutsch. Professionell, freundlich, prägnant, max. 3 Sätze. Keine konkreten Preise nennen.'),
    'fr': ('法语', 'Répondez en français. Professionnel, aimable, concis, maximum 3 phrases. Ne mentionnez pas de prix précis.'),
    'it': ('意大利语', 'Rispondi in italiano. Professionale, cordiale, conciso, massimo 3 frasi. Non indicare prezzi specifici.'),
    'tr': ('土耳其语', 'Türkçe yanıt verin. Profesyonel, samimi, kısa, en fazla 3 cümle. Belirli fiyat vermeyin.'),
    'id': ('印尼语', 'Balas dalam Bahasa Indonesia. Profesional, ramah, singkat, maksimal 3 kalimat. Jangan sebutkan harga spesifik.'),
}

FALLBACK_LANG = 'en', '英语'

def detect_lang(text):
    t = (text or '').strip().lower()
    if re.search(r'[぀-ゟ゠-ヿ]', text or ''): return 'ja'
    if re.search(r'[一-鿿]', text or ''): return 'zh'
    if re.search(r'[가-힯]', text or ''): return 'ko'
    if re.search(r'[؀-ۿ]', text or ''): return 'ar'
    if re.search(r'[Ѐ-ӿ]', text or ''): return 'ru'
    if re.search(r'[฀-๿]', text or ''): return 'th'
    if any(w in t for w in ['xin chào','cảm ơn','giá','báo giá']): return 'vi'
    if any(w in t for w in ['hola','gracias','buenos','precio','cotizacion','catalogo']): return 'es'
    if any(w in t for w in ['obrigado','bom dia','preço','catálogo']): return 'pt'
    if any(w in t for w in ['danke','hallo','bitte','preis','katalog']): return 'de'
    if any(w in t for w in ['bonjour','merci','prix','catalogue']): return 'fr'
    if any(w in t for w in ['ciao','grazie','prezzo','catalogo']): return 'it'
    if any(w in t for w in ['merhaba','teşekkür','fiyat','katalog']): return 'tr'
    if any(w in t for w in ['halo','terima kasih','harga','katalog']): return 'id'
    return 'en'

def get_lang_info(code):
    return LANG_MAP.get(code, FALLBACK_LANG)

FALLBACK_REPLY = {
    'en': "Thanks for your message! We'll get back to you shortly. 🚿",
    'zh': "感谢您的消息！我们会尽快回复您。🚿",
    'ja': "メッセージありがとうございます。まもなくご返信いたします。🚿",
    'ko': "메시지 감사합니다! 곧 답변 드리겠습니다.🚿",
    'es': "¡Gracias por su mensaje! Le responderemos pronto. 🚿",
    'pt': "Obrigado pela sua mensagem! Responderemos em breve. 🚿",
    'de': "Danke für Ihre Nachricht! Wir melden uns in Kürze. 🚿",
    'ru': "Спасибо за ваше сообщение! Мы скоро ответим. 🚿",
    'ar': "شكرًا لرسالتك! سنرد عليك قريبًا. 🚿",
    'vi': "Cảm ơn tin nhắn của bạn! Chúng tôi sẽ phản hồi sớm. 🚿",
    'fr': "Merci pour votre message ! Nous vous répondrons bientôt. 🚿",
    'it': "Grazie per il tuo messaggio! Ti risponderemo presto. 🚿",
    'tr': "Mesajınız için teşekkürler! Yakında size döneceiz. 🚿",
    'id': "Terima kasih atas pesan Anda! Kami akan segera membalas. 🚿",
    'th': "ขอบคุณสำหรับข้อความของคุณ! เราจะตอบกลับโดยเร็วที่สุด 🚿",
}

def get_reply_lang(lang_code):
    _, instr = get_lang_info(lang_code)
    return instr

def infer_lang_from_history(phone, msgs, state):
    profile = state.get('lang_profile', {}).get(phone, {})
    if profile.get('preferred'):
        return profile.get('preferred')
    incoming = [detect_lang(m.get('textMessage','')) for m in msgs or [] if m.get('type')=='incoming']
    for lang in incoming:
        if lang != 'en': return lang
    return incoming[0] if incoming else 'en'

def choose_lang(phone, text, msgs, state):
    detected = detect_lang(text)
    if detected != 'en':
        return detected
    hist = infer_lang_from_history(phone, msgs, state)
    return hist if hist != 'en' else detected

def update_lang_profile(state, phone, lang_code):
    state.setdefault('lang_profile', {})
    p = state['lang_profile'].setdefault(phone, {})
    if not p.get('first_detected'):
        p['first_detected'] = lang_code
    p['last_detected'] = lang_code
    p['preferred'] = lang_code
    p['updated_at'] = datetime.now().isoformat()
    return state


# ============== 核心逻辑 ==============

def generate_reply_and_actions(incoming_text, has_image=False, image_desc="", preferred_lang='en'):
    lang_name, lang_instr = get_lang_info(preferred_lang)
    text_lower = incoming_text.lower()

    actions = []
    if any(k in text_lower for k in ['catalog','pdf','图册','brochure','catalogue','katalog','catálogo']):
        actions.append('send_catalog')
    if any(k in text_lower for k in ['image','photo','图片','picture','款式','imagen','foto','hình ảnh']):
        actions.append('send_image')
    if any(k in text_lower for k in ['video','视频','演示','vídeo','clip']):
        actions.append('send_video')

    action_str = ''
    action_map = {'send_catalog': 'send product catalog PDF', 'send_image': 'send product images', 'send_video': 'send product video'}
    if actions:
        action_str = ' System will: ' + ' + '.join(action_map[a] for a in actions)

    prompt = (
        f"You are a professional B2B sales representative.\n"
        f"Customer message: {incoming_text}\n"
        f"{PRODUCT_INFO}\n"
        + (f"Customer sent an image. Description: {image_desc}\n" if has_image else "")
        + f"{action_str}\n\n"
        f"IMPORTANT: Reply in the customer's language ({lang_name}). {lang_instr}\n"
        f"Output ONLY the reply text, no explanation."
    )

    log(f"🌐 回复语言: {lang_name} ({preferred_lang})，消息: {incoming_text[:40]}")

    reply = ai_generate_reply(prompt)
    if not reply:
        reply = FALLBACK_REPLY.get(preferred_lang, FALLBACK_REPLY['en'])
    return reply, actions

def notify_boss(phone, text):
    log(f"🚨 意向记录 {phone}: {text[:80]}")
    n = json.load(open(NOTIFY_FILE)) if os.path.exists(NOTIFY_FILE) else []
    n.append({'time': datetime.now().isoformat(), 'phone': phone, 'name': phone,
              'message': text, 'text': text})
    json.dump(n, open(NOTIFY_FILE, 'w'), ensure_ascii=False, indent=2)

def get_chat(phone, count=5):
    return api(
        f"{API_URL}/waInstance{INSTANCE_ID}/getChatHistory/{SERVICE_CREDENTIAL}",
        json_data={"chatId": f"{phone}@c.us", "count": count}
    )

def auto_discover(cfg):
    try:
        chats = api(f"{cfg['api_url']}/waInstance{cfg['id_instance']}/getChats/{cfg['service_credential']}", method='GET')
        if not isinstance(chats, list):
            return []
        known = set(json.load(open(CUSTOMERS_FILE)) if os.path.exists(CUSTOMERS_FILE) else [])
        new_found = []
        for chat in chats:
            chat_id = chat.get('id', '')
            if '@g.us' in chat_id or chat_id in ['0@c.us']: continue
            phone = chat_id.replace('@c.us','').replace('@s.whatsapp.net','')
            if not phone or phone in known: continue
            msgs = get_chat(phone, count=5)
            if any(m.get('type')=='incoming' for m in msgs or []):
                new_found.append(phone)
                log(f"🆕 自动发现新回复号码: {phone}")
        if new_found:
            all_p = list(known | set(new_found))
            json.dump(all_p, open(CUSTOMERS_FILE, 'w'), ensure_ascii=False)
            log(f"✅ 联系人列表已更新: {len(all_p)} 个号码")
        return new_found
    except Exception as e:
        log(f"⚠️ 自动发现异常: {e}")
        return []

def process_message(phone, state):
    msgs = get_chat(phone, count=8)
    if not isinstance(msgs, list) or not msgs: return state

    latest = msgs[0]
    latest_id = latest.get('idMessage','')
    latest_type = latest.get('type','')
    latest_text = (latest.get('textMessage') or '').strip()
    msg_data = latest.get('messageData', {})
    file_url = None
    has_image = False

    if latest.get('typeMessage') == 'imageMessage':
        has_image = True
        file_url = msg_data.get('url') or msg_data.get('downloadUrl') or latest.get('downloadUrl')
    elif 'extendedTextMessageData' in msg_data:
        file_url = msg_data['extendedTextMessageData'].get('urlFile') or msg_data['extendedTextMessageData'].get('url')

    baseline_id = state['baseline'].get(phone,'')
    last_reply = state['replied_at'].get(phone, 0)
    now = time.time()

    if latest_id == baseline_id: return state
    if now - last_reply < MIN_REPEAT_WAIT:
        state['baseline'][phone] = latest_id
        return state

    if latest_type == 'incoming' and latest_text:
        lang = choose_lang(phone, latest_text, msgs, state)
        log(f"📥 新文字消息 {phone}: {latest_text[:60]}")

        reply, actions = generate_reply_and_actions(latest_text, has_image=False, preferred_lang=lang)
        send_text(phone, reply)
        state = update_lang_profile(state, phone, lang)

        for cat_path, cat in get_product_files().items():
            if os.path.exists(cat_path):
                send_file_by_upload(phone, cat_path, cat.get('caption',''), os.path.basename(cat_path))
                time.sleep(3)
        if actions:
            for img_key, img in get_product_images().items():
                if img.get('url'):
                    send_file_by_url(phone, img['url'], f"{img_key}.jpg", img.get('caption',''))
                    time.sleep(2)
            for vid_key, vid in get_product_videos().items():
                if vid.get('url'):
                    send_file_by_url(phone, vid['url'], f"{vid_key}.mp4", vid.get('caption',''))
        state['baseline'][phone] = latest_id
        state['replied_at'][phone] = now
        save_state(state)
        if any(kw.lower() in latest_text.lower() for kw in HIGH_INTENT):
            notify_boss(phone, latest_text)
        return state

    if latest_type == 'incoming' and not latest_text and (file_url or has_image):
        log(f"🖼️ 收到图片消息 {phone}")
        img_path = None
        if file_url:
            img_path = os.path.join(WORK_DIR, f'.tmp_img_{phone}.jpg')
            downloaded = download_file(file_url, img_path)
            if downloaded: img_path = downloaded
        image_desc = ""
        if img_path and os.path.exists(img_path):
            image_desc = ai_analyze_image(img_path, context="A customer sent an image for you to analyze.")
        reply = image_desc or "Thanks for sharing! We've received your image and will check it right away. 🚿"
        send_text(phone, reply)
        state['baseline'][phone] = latest_id
        state['replied_at'][phone] = now
        save_state(state)
        return state

    if latest_type == 'incoming' and not latest_text:
        log(f"📎 收到附件消息 {phone}")
        send_text(phone, "Thanks for your message! We've received it and will check right away. 🚿")
        state['baseline'][phone] = latest_id
        state['replied_at'][phone] = now
        save_state(state)
        return state

    state['baseline'][phone] = latest_id
    return state


# ============== 主循环 ==============

def main():
    log("=" * 60)
    log(f"🤖 WhatsApp 全自动跟单系统启动")
    log(f"   版本: configurable-env-v1")
    log(f"   工作目录: {WORK_DIR}")
    log(f"   AI Agent: {AI_AGENT}")
    log("=" * 60)

    state = load_state()

    # 初始化已知号码
    phones = json.load(open(CUSTOMERS_FILE)) if os.path.exists(CUSTOMERS_FILE) else []
    for phone in phones:
        if phone not in state['baseline']:
            msgs = get_chat(phone, count=3)
            if msgs and isinstance(msgs, list):
                state['baseline'][phone] = msgs[0].get('idMessage','')

    log(f"📋 初始监控号码: {len(phones)} 个")
    save_state(state)

    cfg = {'api_url': API_URL, 'id_instance': INSTANCE_ID, 'service_credential': SERVICE_CREDENTIAL}
    poll = 0
    while True:
        poll += 1
        try:
            # 每轮刷新联系人列表
            phones = json.load(open(CUSTOMERS_FILE)) if os.path.exists(CUSTOMERS_FILE) else []

            # 每分钟自动发现一次
            if poll % 12 == 0:
                auto_discover(cfg)

            for phone in phones:
                state = process_message(phone, state)

            if poll % 30 == 0:
                log(f"💓 心跳 {poll}次，监控 {len(phones)} 个号码")
                save_state(state)
        except Exception as e:
            log(f"❌ 异常: {e}")
        time.sleep(5)

if __name__ == '__main__':
    main()
