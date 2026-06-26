export const RELATIVE_HINTS = ['转个身', '换个角度', '还是这套', '同一套', '近一点', '远一点', '坐下', '站起来', '回头'];

export const MIRROR_KEYWORDS = ['wear', 'outfit', 'clothes', 'dress', 'hoodie', 'suit', 'full-body', 'mirror', '全身', '镜子', '穿', 'ootd', '穿搭', '衣服', '卫衣'];
export const DIRECT_KEYWORDS = ['selfie', 'portrait', 'face', 'close-up', '自拍', '怼脸', '近照', '表情'];
export const SELFIE_KEYWORDS = ['selfie', 'photo', 'pic', '自拍', '照片', '发一张', '来一张', '来张'];

export const SCENE_KEYWORDS_BY_TAG = {
  cafe: ['cafe', 'coffee', 'latte', 'espresso', '咖啡', '咖啡店'],
  bookstore: ['bookstore', 'book shop', 'books', '书店', '书架', '看书'],
  mall: ['mall', 'shopping', 'shopping center', '商场', '逛街', '购物'],
  office: ['office', 'work', 'desk', 'feishu', 'lark', '工位', '上班', '公司', '办公室', '飞书'],
  gym: ['gym', 'workout', 'training', '健身', '运动', '有氧'],
  bedroom: ['bedroom', 'bed', 'home', 'pajama', 'sleep', '卧室', '床', '睡衣', '在家', '睡觉'],
  dance: ['dance', 'studio', '舞室', '跳舞', '练舞', '练完舞', '舞蹈'],
  city: ['street', 'city', 'night', 'walk', 'outside', 'downtown', '安福路', '武康路', '街上', '出门', '路上', '夜景'],
  casualIndoor: ['indoor', 'lobby', 'studio lobby', '休闲区', '室内', '大厅']
};

export const PROMPT_SCENE_BY_TAG = {
  cafe: 'cafe',
  bookstore: 'bookstore',
  mall: 'mall',
  office: 'office',
  gym: 'gym',
  bedroom: 'bedroom',
  dance: 'dance studio',
  city: 'city street',
  casualIndoor: 'casual indoor'
};

function pickStableTag(seedText, tags) {
  const normalized = normalizeRequest(seedText || 'weekend');
  const seed = Math.abs([...normalized].reduce((sum, char) => sum + char.charCodeAt(0), 0));
  return tags[seed % tags.length];
}

export function resolveWeekendDaySceneTag(hour, text = '') {
  if (hour < 12) return 'bedroom';
  if (hour < 15) return pickStableTag(text, ['cafe', 'bookstore', 'mall', 'casualIndoor']);
  return 'city';
}

export function normalizeRequest(text = '') {
  return text.trim().toLowerCase();
}

export function hasAny(text, keywords) {
  return keywords.some((keyword) => text.includes(keyword));
}

export function hasRelativeInstruction(text) {
  return hasAny(normalizeRequest(text), RELATIVE_HINTS.map((keyword) => keyword.toLowerCase()));
}

export function detectSceneTag(text) {
  const normalized = normalizeRequest(text);
  if (hasRelativeInstruction(normalized)) return 'relative';
  if (hasAny(normalized, MIRROR_KEYWORDS)) return 'outfit';
  for (const [tag, keywords] of Object.entries(SCENE_KEYWORDS_BY_TAG)) {
    if (hasAny(normalized, keywords)) return tag;
  }
  if (hasAny(normalized, SELFIE_KEYWORDS)) return 'selfie';
  return undefined;
}
