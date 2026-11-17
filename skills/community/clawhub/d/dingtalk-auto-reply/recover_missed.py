"""
钉钉自动回复 · 漏发补发器
用途：监控进程曾宕机 / 处于 DRY_RUN 模式导致单聊未读没被代复时，
      手动把"当前仍未被处理的单聊未读"以本人身份补发一条回复。
强制实时模式（忽略继承来的 DRY_RUN=1），真正发送 + 推微信。

用法：
  <venv>/python.exe recover_missed.py
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dingtalk_unread_monitor as M

# 强制实时：部署监控若继承了 DRY_RUN=1，这里覆盖掉，确保真正发送。
# DRY_RUN 是 runtime 里的可变配置，子模块通过 runtime.DRY_RUN 读取，
# 所以必须改 runtime 模块的属性本身才真正生效（仅设 M.DRY_RUN 是入口副本，不生效）。
import runtime as _rt
_rt.DRY_RUN = False


def main():
    print(f"[recover] DRY_RUN forced = {_rt.DRY_RUN} (live send ON)")
    convs, _health = M.get_unread()  # health 不关心（手动补发，老板自己判断 dws 是否可用）
    print(f"[recover] dws health: {_health}")
    print("[recover] unread convs:")
    print(json.dumps(convs, ensure_ascii=False)[:2000])

    singles = [c for c in convs if c.get("singleChat")]
    if not singles:
        print("[recover] 当前没有单聊未读需要补发。")
        return

    for conv in singles:
        cid = conv.get("openConversationId") or conv.get("conversationId") or conv.get("id")
        msg = M.get_latest_msg(cid)
        sender = M.msg_field(msg, "sender", "senderName", "senderNick")
        content = M._as_text(M.msg_field(msg, "content", "text", "body", default=""))
        sender_open_id = M.extract_sender_open_id(msg)
        msg_id = M.msg_field(msg, "openMessageId", "messageId", "msgId")

        # —— 复用主脚本的图片处理逻辑（避免 mediaId 噪音喂给 AI / 图片消息退化成纯文本）——
        media_ids = M.extract_media_ids(content)
        clean = M.clean_text_for_ai(content)
        body = clean if clean else "(图片/媒体消息)"

        print(f"\n=== 单聊未读 ===\n来自：{sender}\ncid：{cid}\nmsg_id：{msg_id}\n内容：{body}")

        if M._is_self(sender, sender_open_id):
            print("[recover] 跳过：最新一条是老板自己发的。")
            continue
        if not msg_id:
            print("[recover] 跳过：缺 msg_id，无法引用回复。")
            continue

        # 抢答防护：老板当前正活跃在该会话则跳过补发（手动工具也要避免抢老板话）。
        # ⚠️ 2026-08-13 修复：owner_recently_active 返回 True/False/None，None 表示
        # dws 未确认（拉不到最近消息），与 monitor 的「defer 重确认」语义一致——
        # 这里把 None 也视为「不确定」而跳过补发，避免 dws 抖动时抢老板话。
        _active = M.owner_recently_active(cid)
        if _active is True:
            print("[recover] 跳过：老板当前在该会话活跃，避免抢答。")
            continue
        if _active is None:
            print("[recover] 跳过：dws 未能确认老板是否活跃（返回 None），保守跳过补发。")
            continue

        # 下载图片（复用主脚本逻辑），用于看图代复
        img_paths = []
        if media_ids and M.VISION_ENABLED and M.AUTO_REPLY_IMAGE:
            img_paths = [p for p, ok in M.download_images(media_ids, msg_id, cid) if ok]

        reply = M.gen_reply(sender, body, image_paths=img_paths if img_paths else None)
        print(f"[recover] 生成回复：{reply}")
        if not reply:
            print("[recover] 未生成有效回复，跳过。")
            continue

        ok = M.send_reply(cid, msg_id, sender_open_id, reply)
        print(f"[recover] 发送结果 ok={ok}")
        M.push_weixin(
            f"🔔 钉钉新消息（单聊·已补发）\n来自：{sender}\n内容：{body[:200]}\n\n🤖 已代复：{reply[:200]}"
        )
        print("[recover] 微信通知已推。")


if __name__ == "__main__":
    main()
