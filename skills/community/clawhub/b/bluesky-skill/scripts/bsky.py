#!/usr/bin/env python3
"""CLI tool for Bluesky/AT Protocol operations. All output is JSON."""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from atproto import Client, IdResolver, client_utils, models


load_dotenv()

SESSION_FILE = Path.home() / ".bsky_session.json"


# --- Output utilities ---

def output_json(data):
    """Print data as JSON to stdout."""
    print(json.dumps(data, default=str))


def error_json(error, message, error_type=None):
    """Print error as JSON to stdout and exit with code 1."""
    d = {"error": error, "message": message}
    if error_type:
        d["type"] = error_type
    print(json.dumps(d))
    sys.exit(1)


# --- Auth ---

def get_client():
    """Create and authenticate a Bluesky client with session caching."""
    handle = os.environ.get("BLUESKY_HANDLE")
    password = os.environ.get("BLUESKY_APP_PASSWORD")

    if not handle or not password:
        error_json("AUTH_ERROR", "Set BLUESKY_HANDLE and BLUESKY_APP_PASSWORD in .env", "MISSING_ENV")

    client = Client()

    def _save_session(event, session):
        """Save session to disk on change."""
        try:
            SESSION_FILE.write_text(json.dumps({"session_string": session.export()}))
        except Exception:
            pass

    client.on_session_change(_save_session)

    # Try cached session first
    if SESSION_FILE.exists():
        try:
            data = json.loads(SESSION_FILE.read_text())
            client.login(session_string=data["session_string"])
            return client
        except Exception:
            SESSION_FILE.unlink(missing_ok=True)

    # Fresh login
    try:
        client.login(handle, password)
        return client
    except Exception as e:
        err = str(e).lower()
        if "suspend" in err or "deactivat" in err:
            error_json("AUTH_ERROR", f"Account issue: {e}", "ACCOUNT_SUSPENDED")
        elif "invalid" in err or "auth" in err or "password" in err or "401" in err:
            error_json("AUTH_ERROR", f"Login failed: {e}", "INVALID_CREDENTIALS")
        elif "network" in err or "connection" in err or "timeout" in err or "dns" in err:
            error_json("AUTH_ERROR", f"Cannot reach Bluesky servers: {e}", "NETWORK")
        else:
            error_json("AUTH_ERROR", f"Login failed: {e}", "UNKNOWN")


# --- Dict builders ---

def embed_to_dict(embed):
    """Convert a post embed to a dict."""
    if not embed:
        return None
    d = {}
    # Images
    if hasattr(embed, "images"):
        d["images"] = [
            {"alt": img.alt or "", "thumb": getattr(img, "thumb", None), "fullsize": getattr(img, "fullsize", None)}
            for img in embed.images
        ]
    # External link
    if hasattr(embed, "external") and embed.external:
        ext = embed.external
        d["external"] = {"uri": ext.uri, "title": getattr(ext, "title", ""), "description": getattr(ext, "description", "")}
    # Quoted record
    if hasattr(embed, "record"):
        rec = embed.record
        if hasattr(rec, "uri"):
            d["record"] = {"uri": rec.uri, "cid": getattr(rec, "cid", None)}
            # If it's a full record view with nested value
            if hasattr(rec, "value") and hasattr(rec.value, "text"):
                d["record"]["text"] = rec.value.text
            if hasattr(rec, "author"):
                d["record"]["author"] = actor_to_dict(rec.author)
    # Record with media (quote + images)
    if hasattr(embed, "media"):
        d.update(embed_to_dict(embed.media) or {})
    return d or None


def actor_to_dict(actor):
    """Convert an actor/author to a short dict."""
    return {
        "handle": actor.handle,
        "did": actor.did,
        "display_name": getattr(actor, "display_name", None) or "",
        "avatar": getattr(actor, "avatar", None),
    }


def post_to_dict(post):
    """Convert a post to a dict."""
    record = getattr(post, "record", None)
    viewer = getattr(post, "viewer", None)
    embed = getattr(post, "embed", None)
    reply = getattr(record, "reply", None) if record else None
    d = {
        "uri": post.uri,
        "cid": post.cid,
        "author": actor_to_dict(post.author),
        "text": getattr(record, "text", "") if record else "",
        "created_at": getattr(record, "created_at", None) if record else None,
        "like_count": post.like_count or 0,
        "repost_count": post.repost_count or 0,
        "reply_count": post.reply_count or 0,
        "viewer": {
            "liked": getattr(viewer, "like", None) if viewer else None,
            "reposted": getattr(viewer, "repost", None) if viewer else None,
        },
        "embed": embed_to_dict(embed),
    }
    if reply:
        d["reply"] = {
            "parent_uri": getattr(reply.parent, "uri", None) if hasattr(reply, "parent") else None,
            "root_uri": getattr(reply.root, "uri", None) if hasattr(reply, "root") else None,
        }
    return d


def profile_to_dict(profile):
    """Convert a profile to a full dict."""
    viewer = getattr(profile, "viewer", None)
    return {
        "handle": profile.handle,
        "did": profile.did,
        "display_name": getattr(profile, "display_name", None) or "",
        "description": getattr(profile, "description", None) or "",
        "avatar": getattr(profile, "avatar", None),
        "followers_count": getattr(profile, "followers_count", 0) or 0,
        "follows_count": getattr(profile, "follows_count", 0) or 0,
        "posts_count": getattr(profile, "posts_count", 0) or 0,
        "viewer": {
            "following": getattr(viewer, "following", None),
            "followed_by": getattr(viewer, "followed_by", None),
            "blocked_by": getattr(viewer, "blocked_by", None),
            "blocking": getattr(viewer, "blocking", None),
            "muted": getattr(viewer, "muted", None),
        } if viewer else None,
    }


def notification_to_dict(notif):
    """Convert a notification to a dict."""
    d = {
        "reason": notif.reason,
        "uri": notif.uri,
        "cid": getattr(notif, "cid", None),
        "is_read": notif.is_read,
        "indexed_at": getattr(notif, "indexed_at", None),
        "author": actor_to_dict(notif.author),
    }
    if hasattr(notif, "record") and notif.record and hasattr(notif.record, "text"):
        d["record_text"] = notif.record.text
    if hasattr(notif, "reason_subject") and notif.reason_subject:
        d["reason_subject"] = notif.reason_subject
    return d


def convo_to_dict(convo):
    """Convert a conversation to a dict."""
    d = {
        "id": convo.id,
        "unread_count": getattr(convo, "unread_count", 0) or 0,
        "members": [actor_to_dict(m) for m in convo.members],
        "last_message": None,
    }
    if hasattr(convo, "last_message") and convo.last_message and hasattr(convo.last_message, "text"):
        msg = convo.last_message
        d["last_message"] = {
            "id": getattr(msg, "id", None),
            "text": msg.text,
            "sent_at": getattr(msg, "sent_at", None),
            "sender_did": getattr(msg.sender, "did", None) if getattr(msg, "sender", None) else None,
        }
    return d


def dm_to_dict(msg):
    """Convert a DM message to a dict."""
    sender = getattr(msg, "sender", None)
    return {
        "id": getattr(msg, "id", None),
        "text": getattr(msg, "text", ""),
        "sent_at": getattr(msg, "sent_at", None),
        "sender_did": sender.did if sender else None,
    }


def feed_to_dict(feed):
    """Convert a feed generator view to a dict."""
    return {
        "uri": feed.uri,
        "cid": feed.cid,
        "did": feed.did,
        "creator": actor_to_dict(feed.creator),
        "display_name": feed.display_name,
        "description": getattr(feed, "description", None) or "",
        "avatar": getattr(feed, "avatar", None),
        "like_count": getattr(feed, "like_count", 0) or 0,
        "indexed_at": getattr(feed, "indexed_at", None),
    }


# --- Helpers ---

def parse_rich_text(client, text):
    """Parse @mentions, #hashtags, and URLs into a TextBuilder."""
    pattern = re.compile(
        r'(@[\w.\-]+)'        # @handle
        r'|(#[\w]+)'           # #hashtag
        r'|(https?://\S+)'    # URL
    )
    tb = client_utils.TextBuilder()
    last_end = 0
    for m in pattern.finditer(text):
        if m.start() > last_end:
            tb.text(text[last_end:m.start()])
        mention, hashtag, url = m.groups()
        if mention:
            handle = mention[1:]
            try:
                profile = client.get_profile(handle)
                tb.mention(mention, profile.did)
            except Exception:
                tb.text(mention)
        elif hashtag:
            tb.tag(hashtag, hashtag[1:])
        elif url:
            tb.link(url, url)
        last_end = m.end()
    if last_end < len(text):
        tb.text(text[last_end:])
    return tb


def get_dm_client(client):
    """Create a chat-proxied client for DM operations."""
    return client.with_bsky_chat_proxy()


# --- Commands ---

def cmd_post(client, args):
    """Create a new post."""
    reply_ref = None
    if args.reply_to:
        parent_resp = client.get_posts([args.reply_to])
        if not parent_resp.posts:
            error_json("NOT_FOUND", f"Post not found: {args.reply_to}")
        parent = parent_resp.posts[0]
        parent_ref = models.create_strong_ref(parent)
        root_ref = parent_ref
        if hasattr(parent.record, "reply") and parent.record.reply:
            root_ref = parent.record.reply.root
        reply_ref = models.AppBskyFeedPost.ReplyRef(parent=parent_ref, root=root_ref)

    embed = None
    if args.quote:
        quote_resp = client.get_posts([args.quote])
        if not quote_resp.posts:
            error_json("NOT_FOUND", f"Post not found: {args.quote}")
        quote_post = quote_resp.posts[0]
        embed = models.AppBskyEmbedRecord.Main(record=models.create_strong_ref(quote_post))

    if args.image:
        if len(args.image) > 4:
            error_json("INVALID_ARGS", "Maximum 4 images per post")
        alts = args.alt or []
        images = []
        for i, img_file in enumerate(args.image):
            img_path = Path(img_file)
            if not img_path.exists():
                error_json("FILE_NOT_FOUND", f"Image not found: {img_file}")
            upload = client.upload_blob(img_path.read_bytes())
            alt = alts[i] if i < len(alts) else ""
            images.append(models.AppBskyEmbedImages.Image(alt=alt, image=upload.blob))
        img_embed = models.AppBskyEmbedImages.Main(images=images)
        if embed:
            embed = models.AppBskyEmbedRecordWithMedia.Main(record=embed, media=img_embed)
        else:
            embed = img_embed

    rich_text = parse_rich_text(client, args.text)
    resp = client.send_post(rich_text, reply_to=reply_ref, embed=embed)
    output_json({"uri": resp.uri, "cid": resp.cid})


def cmd_delete(client, args):
    """Delete a post by URI."""
    client.delete_post(args.uri)
    output_json({"deleted": args.uri})


def cmd_like(client, args):
    """Like a post."""
    resp = client.get_posts([args.uri])
    if not resp.posts:
        error_json("NOT_FOUND", f"Post not found: {args.uri}")
    post = resp.posts[0]
    like = client.like(uri=post.uri, cid=post.cid)
    output_json({"liked": args.uri, "uri": like.uri})


def cmd_unlike(client, args):
    """Unlike a post by its post URI."""
    resp = client.get_posts([args.uri])
    if not resp.posts:
        error_json("NOT_FOUND", f"Post not found: {args.uri}")
    post = resp.posts[0]
    viewer = getattr(post, "viewer", None)
    like_uri = getattr(viewer, "like", None) if viewer else None
    if not like_uri:
        error_json("NOT_LIKED", f"Post not liked: {args.uri}")
    client.unlike(like_uri)
    output_json({"unliked": args.uri})


def cmd_repost(client, args):
    """Repost a post."""
    resp = client.get_posts([args.uri])
    if not resp.posts:
        error_json("NOT_FOUND", f"Post not found: {args.uri}")
    post = resp.posts[0]
    repost = client.repost(uri=post.uri, cid=post.cid)
    output_json({"reposted": args.uri, "uri": repost.uri})


def cmd_unrepost(client, args):
    """Undo a repost by post URI."""
    resp = client.get_posts([args.uri])
    if not resp.posts:
        error_json("NOT_FOUND", f"Post not found: {args.uri}")
    post = resp.posts[0]
    viewer = getattr(post, "viewer", None)
    repost_uri = getattr(viewer, "repost", None) if viewer else None
    if not repost_uri:
        error_json("NOT_REPOSTED", f"Post not reposted: {args.uri}")
    client.unrepost(repost_uri)
    output_json({"unreposted": args.uri})


def cmd_timeline(client, args):
    """Show home timeline."""
    params = {"limit": args.limit}
    if args.cursor:
        params["cursor"] = args.cursor
    resp = client.get_timeline(**params)
    feed = []
    for item in resp.feed:
        entry = {"post": post_to_dict(item.post)}
        if item.reason and hasattr(item.reason, "by"):
            entry["reason"] = {"type": "repost", "by": actor_to_dict(item.reason.by)}
        feed.append(entry)
    output_json({"feed": feed, "cursor": getattr(resp, "cursor", None)})


def cmd_thread(client, args):
    """View a post thread."""
    resp = client.get_post_thread(uri=args.uri, depth=args.depth)

    def _thread_to_dict(node):
        """Convert a thread node to a dict recursively."""
        if not hasattr(node, "post"):
            return None
        d = post_to_dict(node.post)
        replies = []
        for r in getattr(node, "replies", []) or []:
            rd = _thread_to_dict(r)
            if rd:
                replies.append(rd)
        d["replies"] = replies
        return d

    output_json({"thread": _thread_to_dict(resp.thread)})


def cmd_search_posts(client, args):
    """Search for posts."""
    params = {"q": args.query, "limit": args.limit}
    if args.cursor:
        params["cursor"] = args.cursor
    resp = client.app.bsky.feed.search_posts(params=params)
    output_json({
        "posts": [post_to_dict(p) for p in resp.posts],
        "cursor": getattr(resp, "cursor", None),
    })


def cmd_search_users(client, args):
    """Search for users."""
    params = {"q": args.query, "limit": args.limit}
    if args.cursor:
        params["cursor"] = args.cursor
    resp = client.app.bsky.actor.search_actors(params=params)
    output_json({
        "actors": [profile_to_dict(a) for a in resp.actors],
        "cursor": getattr(resp, "cursor", None),
    })


def cmd_follow(client, args):
    """Follow an account."""
    profile = client.get_profile(args.handle)
    resp = client.follow(profile.did)
    output_json({"followed": args.handle, "uri": resp.uri})


def cmd_unfollow(client, args):
    """Unfollow an account."""
    profile = client.get_profile(args.handle)
    viewer = getattr(profile, "viewer", None)
    follow_uri = getattr(viewer, "following", None) if viewer else None
    if not follow_uri:
        error_json("NOT_FOLLOWING", f"Not following @{args.handle}")
    client.unfollow(follow_uri)
    output_json({"unfollowed": args.handle})


def cmd_followers(client, args):
    """List followers."""
    params = {"actor": args.handle, "limit": args.limit}
    if args.cursor:
        params["cursor"] = args.cursor
    resp = client.get_followers(**params)
    output_json({
        "followers": [actor_to_dict(f) for f in resp.followers],
        "cursor": getattr(resp, "cursor", None),
    })


def cmd_following(client, args):
    """List accounts being followed."""
    params = {"actor": args.handle, "limit": args.limit}
    if args.cursor:
        params["cursor"] = args.cursor
    resp = client.get_follows(**params)
    output_json({
        "following": [actor_to_dict(f) for f in resp.follows],
        "cursor": getattr(resp, "cursor", None),
    })


def cmd_mute(client, args):
    """Mute an account."""
    client.mute(args.handle)
    output_json({"muted": args.handle})


def cmd_unmute(client, args):
    """Unmute an account."""
    client.unmute(args.handle)
    output_json({"unmuted": args.handle})


def cmd_block(client, args):
    """Block an account."""
    profile = client.get_profile(args.handle)
    resp = client.app.bsky.graph.block.create(
        client.me.did,
        models.AppBskyGraphBlock.Record(
            subject=profile.did,
            created_at=client.get_current_time_iso(),
        ),
    )
    output_json({"blocked": args.handle, "uri": resp.uri})


def cmd_unblock(client, args):
    """Unblock an account."""
    profile = client.get_profile(args.handle)
    viewer = getattr(profile, "viewer", None)
    block_uri = getattr(viewer, "blocking", None) if viewer else None
    if not block_uri:
        error_json("NOT_BLOCKING", f"Not blocking @{args.handle}")
    rkey = block_uri.split("/")[-1]
    client.app.bsky.graph.block.delete(client.me.did, rkey)
    output_json({"unblocked": args.handle})


def cmd_profile(client, args):
    """View a profile."""
    handle = args.handle or client.me.handle
    profile = client.get_profile(handle)
    output_json(profile_to_dict(profile))


def cmd_likes(client, args):
    """Show who liked a post."""
    params = {"uri": args.uri, "limit": args.limit}
    if args.cursor:
        params["cursor"] = args.cursor
    resp = client.get_likes(**params)
    output_json({
        "likes": [{"actor": actor_to_dict(like.actor), "created_at": getattr(like, "created_at", None)} for like in resp.likes],
        "cursor": getattr(resp, "cursor", None),
    })


def cmd_reposts(client, args):
    """Show who reposted a post."""
    params = {"uri": args.uri, "limit": args.limit}
    if args.cursor:
        params["cursor"] = args.cursor
    resp = client.get_reposted_by(**params)
    output_json({
        "reposted_by": [actor_to_dict(a) for a in resp.reposted_by],
        "cursor": getattr(resp, "cursor", None),
    })


def cmd_get(client, args):
    """Fetch a single post by URI."""
    resp = client.get_posts([args.uri])
    if not resp.posts:
        error_json("NOT_FOUND", f"Post not found: {args.uri}")
    output_json(post_to_dict(resp.posts[0]))


def cmd_my_posts(client, args):
    """Show own recent posts."""
    params = {"actor": client.me.did, "limit": args.limit}
    if args.cursor:
        params["cursor"] = args.cursor
    resp = client.app.bsky.feed.get_author_feed(params=params)
    output_json({
        "posts": [post_to_dict(item.post) for item in resp.feed],
        "cursor": getattr(resp, "cursor", None),
    })


def cmd_user_posts(client, args):
    """Show a user's recent posts."""
    params = {"actor": args.handle, "limit": args.limit}
    if args.cursor:
        params["cursor"] = args.cursor
    resp = client.app.bsky.feed.get_author_feed(params=params)
    output_json({
        "posts": [post_to_dict(item.post) for item in resp.feed],
        "cursor": getattr(resp, "cursor", None),
    })


def cmd_notifications(client, args):
    """List notifications."""
    params = {"limit": args.limit}
    if args.cursor:
        params["cursor"] = args.cursor
    resp = client.app.bsky.notification.list_notifications(params=params)
    notifs = []
    for notif in resp.notifications:
        if args.unread_only and notif.is_read:
            continue
        if args.filter and notif.reason != args.filter:
            continue
        notifs.append(notification_to_dict(notif))
    # Batch-fetch subject posts for richer context
    subject_uris = list({n["reason_subject"] for n in notifs if n.get("reason_subject")})
    if subject_uris:
        subject_texts = {}
        for i in range(0, len(subject_uris), 25):
            posts_resp = client.get_posts(subject_uris[i:i + 25])
            for p in posts_resp.posts:
                subject_texts[p.uri] = getattr(p.record, "text", "") if hasattr(p, "record") else ""
        for n in notifs:
            if n.get("reason_subject") in subject_texts:
                n["subject_text"] = subject_texts[n["reason_subject"]]
    output_json({
        "notifications": notifs,
        "cursor": getattr(resp, "cursor", None),
    })


def cmd_notif_read(client, args):
    """Mark all notifications as read."""
    client.app.bsky.notification.update_seen(
        data={"seen_at": datetime.now(timezone.utc).isoformat()}
    )
    output_json({"success": True})


# --- DM Commands ---

def cmd_dm_list(client, args):
    """List DM conversations."""
    dm = get_dm_client(client)
    params = {"limit": args.limit}
    if args.cursor:
        params["cursor"] = args.cursor
    resp = dm.chat.bsky.convo.list_convos(
        models.ChatBskyConvoListConvos.Params(**params)
    )
    output_json({
        "conversations": [convo_to_dict(c) for c in resp.convos],
        "cursor": getattr(resp, "cursor", None),
    })


def cmd_dm_read(client, args):
    """Read messages in a DM conversation."""
    dm = get_dm_client(client)
    if args.handle:
        resolver = IdResolver()
        did = resolver.handle.resolve(args.handle)
        convo = dm.chat.bsky.convo.get_convo_for_members(
            models.ChatBskyConvoGetConvoForMembers.Params(members=[did])
        ).convo
        convo_id = convo.id
    else:
        convo_id = args.convo_id

    params = {"convo_id": convo_id, "limit": args.limit}
    if args.cursor:
        params["cursor"] = args.cursor
    resp = dm.chat.bsky.convo.get_messages(
        models.ChatBskyConvoGetMessages.Params(**params)
    )
    messages = [dm_to_dict(msg) for msg in resp.messages if hasattr(msg, "text")]
    output_json({
        "convo_id": convo_id,
        "messages": messages,
        "cursor": getattr(resp, "cursor", None),
    })


def cmd_dm_send(client, args):
    """Send a DM to a user."""
    dm = get_dm_client(client)
    resolver = IdResolver()
    did = resolver.handle.resolve(args.handle)
    convo = dm.chat.bsky.convo.get_convo_for_members(
        models.ChatBskyConvoGetConvoForMembers.Params(members=[did])
    ).convo
    resp = dm.chat.bsky.convo.send_message(
        models.ChatBskyConvoSendMessage.Data(
            convo_id=convo.id,
            message=models.ChatBskyConvoDefs.MessageInput(text=args.text),
        )
    )
    output_json({"sent": True, "convo_id": convo.id, "message_id": getattr(resp, "id", None)})


def cmd_dm_mark_read(client, args):
    """Mark a DM conversation as read."""
    dm = get_dm_client(client)
    if args.all:
        dm.chat.bsky.convo.update_all_read()
        output_json({"success": True})
    else:
        dm.chat.bsky.convo.update_read(
            models.ChatBskyConvoUpdateRead.Data(convo_id=args.convo_id)
        )
        output_json({"success": True, "convo_id": args.convo_id})


def cmd_update_profile(client, args):
    """Update the authenticated user's profile."""
    if not args.name and not args.bio and not args.avatar:
        error_json("INVALID_ARGS", "Provide at least one of --name, --bio, --avatar")
    current = client.com.atproto.repo.get_record(
        models.ComAtprotoRepoGetRecord.Params(
            repo=client.me.did,
            collection="app.bsky.actor.profile",
            rkey="self",
        )
    )
    record = current.value
    if args.name is not None:
        record["displayName"] = args.name
    if args.bio is not None:
        record["description"] = args.bio
    if args.avatar:
        with open(args.avatar, "rb") as f:
            img_data = f.read()
        resp = client.upload_blob(img_data)
        record["avatar"] = resp.blob
    client.com.atproto.repo.put_record(
        models.ComAtprotoRepoPutRecord.Data(
            repo=client.me.did,
            collection="app.bsky.actor.profile",
            rkey="self",
            record=record,
        )
    )
    profile = client.get_profile(client.me.handle)
    output_json(profile_to_dict(profile))


def cmd_post_thread(client, args):
    """Create a multi-post thread."""
    posts = []
    root_ref = None
    parent_ref = None
    for i, text in enumerate(args.texts):
        rich_text = parse_rich_text(client, text)
        reply_ref = None
        if i > 0:
            reply_ref = models.AppBskyFeedPost.ReplyRef(
                parent=parent_ref, root=root_ref
            )
        resp = client.send_post(rich_text, reply_to=reply_ref)
        ref = models.ComAtprotoRepoStrongRef.Main(uri=resp.uri, cid=resp.cid)
        if i == 0:
            root_ref = ref
        parent_ref = ref
        posts.append({"uri": resp.uri, "cid": resp.cid})
    output_json({"posts": posts})


def cmd_feeds(client, args):
    """List suggested feed generators."""
    params = {"limit": args.limit}
    if args.cursor:
        params["cursor"] = args.cursor
    resp = client.app.bsky.feed.get_suggested_feeds(params=params)
    feeds = [feed_to_dict(f) for f in resp.feeds]
    if args.query:
        q = args.query.lower()
        feeds = [f for f in feeds if q in f["display_name"].lower() or q in f["description"].lower()]
    output_json({"feeds": feeds, "cursor": getattr(resp, "cursor", None)})


# --- Main ---

def main():
    """Parse arguments and dispatch to command handler."""
    parser = argparse.ArgumentParser(description="Bluesky CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    # post
    p = sub.add_parser("post", help="Create a post")
    p.add_argument("text", help="Post text (max 300 graphemes)")
    p.add_argument("--image", action="append", help="Image file (up to 4, repeat flag)")
    p.add_argument("--alt", action="append", help="Alt text per image (same order)")
    p.add_argument("--reply-to", help="URI of post to reply to")
    p.add_argument("--quote", help="URI of post to quote")

    # post-thread
    p = sub.add_parser("post-thread", help="Create a multi-post thread")
    p.add_argument("texts", nargs="+", help="Text for each post in the thread")

    # delete
    p = sub.add_parser("delete", help="Delete a post")
    p.add_argument("uri", help="Post URI")

    # like / unlike
    p = sub.add_parser("like", help="Like a post")
    p.add_argument("uri", help="Post URI")
    p = sub.add_parser("unlike", help="Unlike a post")
    p.add_argument("uri", help="Post URI")

    # repost / unrepost
    p = sub.add_parser("repost", help="Repost a post")
    p.add_argument("uri", help="Post URI")
    p = sub.add_parser("unrepost", help="Undo a repost")
    p.add_argument("uri", help="Post URI")

    # timeline
    p = sub.add_parser("timeline", help="Show home timeline")
    p.add_argument("--limit", type=int, default=20, help="Number of posts")
    p.add_argument("--cursor", help="Pagination cursor")

    # thread
    p = sub.add_parser("thread", help="View a post thread")
    p.add_argument("uri", help="Post URI")
    p.add_argument("--depth", type=int, default=6, help="Reply depth")

    # search
    p = sub.add_parser("search-posts", help="Search posts")
    p.add_argument("query", help="Search query")
    p.add_argument("--limit", type=int, default=20, help="Number of results")
    p.add_argument("--cursor", help="Pagination cursor")
    p = sub.add_parser("search-users", help="Search users")
    p.add_argument("query", help="Search query")
    p.add_argument("--limit", type=int, default=20, help="Number of results")
    p.add_argument("--cursor", help="Pagination cursor")

    # feeds
    p = sub.add_parser("feeds", help="Browse suggested feed generators")
    p.add_argument("--query", help="Filter feeds by keyword")
    p.add_argument("--limit", type=int, default=25, help="Number of feeds")
    p.add_argument("--cursor", help="Pagination cursor")

    # social graph
    p = sub.add_parser("follow", help="Follow an account")
    p.add_argument("handle", help="Handle to follow")
    p = sub.add_parser("unfollow", help="Unfollow an account")
    p.add_argument("handle", help="Handle to unfollow")
    p = sub.add_parser("followers", help="List followers")
    p.add_argument("handle", help="Handle to check")
    p.add_argument("--limit", type=int, default=50, help="Number of results")
    p.add_argument("--cursor", help="Pagination cursor")
    p = sub.add_parser("following", help="List following")
    p.add_argument("handle", help="Handle to check")
    p.add_argument("--limit", type=int, default=50, help="Number of results")
    p.add_argument("--cursor", help="Pagination cursor")

    # mute / block
    p = sub.add_parser("mute", help="Mute an account")
    p.add_argument("handle", help="Handle to mute")
    p = sub.add_parser("unmute", help="Unmute an account")
    p.add_argument("handle", help="Handle to unmute")
    p = sub.add_parser("block", help="Block an account")
    p.add_argument("handle", help="Handle to block")
    p = sub.add_parser("unblock", help="Unblock an account")
    p.add_argument("handle", help="Handle to unblock")

    # profile
    p = sub.add_parser("profile", help="View profile")
    p.add_argument("handle", nargs="?", help="Handle (own profile if omitted)")

    # update-profile
    p = sub.add_parser("update-profile", help="Update your profile")
    p.add_argument("--name", help="Display name")
    p.add_argument("--bio", help="Bio / description")
    p.add_argument("--avatar", help="Path to avatar image")

    # info
    p = sub.add_parser("likes", help="Who liked a post")
    p.add_argument("uri", help="Post URI")
    p.add_argument("--limit", type=int, default=50, help="Number of results")
    p.add_argument("--cursor", help="Pagination cursor")
    p = sub.add_parser("reposts", help="Who reposted a post")
    p.add_argument("uri", help="Post URI")
    p.add_argument("--limit", type=int, default=50, help="Number of results")
    p.add_argument("--cursor", help="Pagination cursor")

    # get single post
    p = sub.add_parser("get", help="Fetch a single post")
    p.add_argument("uri", help="Post URI")

    # my-posts
    p = sub.add_parser("my-posts", help="Show own recent posts")
    p.add_argument("--limit", type=int, default=20, help="Number of posts")
    p.add_argument("--cursor", help="Pagination cursor")

    # user-posts
    p = sub.add_parser("user-posts", help="Show a user's recent posts")
    p.add_argument("handle", help="Handle to check")
    p.add_argument("--limit", type=int, default=20, help="Number of posts")
    p.add_argument("--cursor", help="Pagination cursor")

    # notifications
    p = sub.add_parser("notifications", help="List notifications")
    p.add_argument("--limit", type=int, default=25, help="Number of results")
    p.add_argument("--unread-only", action="store_true", help="Show only unread")
    p.add_argument("--filter", choices=["like", "repost", "follow", "mention", "reply", "quote"], help="Filter by type")
    p.add_argument("--cursor", help="Pagination cursor")
    sub.add_parser("notif-read", help="Mark all notifications as read")

    # DMs
    p = sub.add_parser("dm-list", help="List DM conversations")
    p.add_argument("--limit", type=int, default=20, help="Number of conversations")
    p.add_argument("--cursor", help="Pagination cursor")
    p = sub.add_parser("dm-read", help="Read messages in a conversation")
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--handle", help="Handle to read DMs with")
    group.add_argument("--convo-id", help="Conversation ID")
    p.add_argument("--limit", type=int, default=25, help="Number of messages")
    p.add_argument("--cursor", help="Pagination cursor")
    p = sub.add_parser("dm-send", help="Send a DM")
    p.add_argument("handle", help="Handle to message")
    p.add_argument("text", help="Message text")
    p = sub.add_parser("dm-mark-read", help="Mark DM conversation as read")
    p.add_argument("--convo-id", help="Conversation ID (omit with --all)")
    p.add_argument("--all", action="store_true", help="Mark all conversations as read")

    args = parser.parse_args()

    # Dispatch
    client = get_client()
    commands = {
        "post": cmd_post, "delete": cmd_delete,
        "like": cmd_like, "unlike": cmd_unlike,
        "repost": cmd_repost, "unrepost": cmd_unrepost,
        "timeline": cmd_timeline, "thread": cmd_thread,
        "search-posts": cmd_search_posts, "search-users": cmd_search_users,
        "follow": cmd_follow, "unfollow": cmd_unfollow,
        "followers": cmd_followers, "following": cmd_following,
        "mute": cmd_mute, "unmute": cmd_unmute,
        "block": cmd_block, "unblock": cmd_unblock,
        "profile": cmd_profile, "get": cmd_get,
        "my-posts": cmd_my_posts, "user-posts": cmd_user_posts,
        "likes": cmd_likes, "reposts": cmd_reposts,
        "notifications": cmd_notifications, "notif-read": cmd_notif_read,
        "dm-list": cmd_dm_list, "dm-read": cmd_dm_read,
        "dm-send": cmd_dm_send, "dm-mark-read": cmd_dm_mark_read,
        "update-profile": cmd_update_profile, "post-thread": cmd_post_thread,
        "feeds": cmd_feeds,
    }
    commands[args.command](client, args)


if __name__ == "__main__":
    main()
