import os

from src.ecommerce_voice_cs import EcommerceVoiceCSSkill

DEFAULT_VOICE_ID = "child_0001_b"


def main() -> None:
    skill = EcommerceVoiceCSSkill()
    api_key = os.getenv("SENSEAUDIO_API_KEY")
    if api_key:
        skill.set_api_key(api_key)
    clone_api_url = os.getenv("SENSEAUDIO_CLONE_API_URL")
    if clone_api_url:
        skill.set_clone_api_url(clone_api_url)

    skill.configure(
        refund_policy="商品签收后 7 天内可退换，质量问题优先处理",
        unboxing_allowed=False,
        shipping_fee_by="商家",
        audio_output_path="./tts_output",
    )

    response = skill.handle_message("我需要你现在当一个客服机器人")
    print(response)

    response = skill.handle_message(
        "我拆了能退吗？",
        voice_handle=os.getenv("SENSEAUDIO_VOICE_ID", DEFAULT_VOICE_ID),
        audio_format=".wav",
    )
    print(response)


if __name__ == "__main__":
    main()
