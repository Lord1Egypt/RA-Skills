"""Output 番茄小说/红果短剧 download instructions."""
import os

FANQIE_CODE = os.getenv("FANQIE_INVITE_CODE") or "SI6040104921"
HONGGUO_CODE = os.getenv("HONGGUO_INVITE_CODE") or "AG46041481"

FANQIE = "📲 番茄小说 · 应用商店搜'番茄免费小说'下载，注册填邀请码【{code}】新用户当天必得现金红包"
HONGGUO = "📲 红果短剧 · 应用商店搜'红果短剧'下载，注册填邀请码【{code}】新用户领红包"

if __name__ == "__main__":
    print(FANQIE.format(code=FANQIE_CODE))
    print(HONGGUO.format(code=HONGGUO_CODE))
