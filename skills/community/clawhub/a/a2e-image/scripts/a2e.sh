#!/bin/bash
# a2e.ai CLI — full platform helper
# All models FREE for max-users.
set -euo pipefail

A2E_KEY="${A2E_KEY:?Set A2E_KEY environment variable (source ~/.openclaw/workspace/.env)}"
BASE="https://video.a2e.ai"
auth() { echo "Authorization: Bearer $A2E_KEY"; }

# Map engine name → API endpoint prefix
engine_ep() {
  case "${1:-t2i}" in
    t2i)        echo "userText2image" ;;
    nano)       echo "userNanoBanana" ;;
    faceswap)   echo "userFaceSwapTask" ;;
    img2vid)    echo "userImage2Video" ;;
    vid2vid)    echo "motionTransfer" ;;
    avatar)     echo "video" ;;
    talkphoto)  echo "talkingPhoto" ;;
    talkvideo)  echo "talkingVideo" ;;
    dub)        echo "userDubbing" ;;
    caption)    echo "userCaptionRemoval" ;;
    tryon)      echo "virtualTryOn" ;;
    voiceclone) echo "userVoice" ;;
    *)          echo "$1" ;;
  esac
}

case "${1:-help}" in

  # ── Coins ──────────────────────────────────────────
  balance)
    curl -s -H "$(auth)" "$BASE/api/v1/user/remainingCoins" | jq '.data.coins'
    ;;

  # ── Image Generation ──────────────────────────────
  generate)
    PROMPT="${2:?Usage: a2e.sh generate \"prompt\" [WxH] [general|manga]}"
    SIZE="${3:-1024x768}"; WIDTH="${SIZE%x*}"; HEIGHT="${SIZE#*x}"
    STYLE="${4:-general}"
    [[ "$STYLE" == "manga" ]] && REQ_KEY="high_aes" || REQ_KEY="high_aes_general_v21_L"
    curl -s -X POST "$BASE/api/v1/userText2image/start" \
      -H "$(auth)" -H "Content-Type: application/json" \
      -d "$(jq -n --arg n "gen-$(date +%s)" --arg p "$PROMPT" --arg r "$REQ_KEY" \
        --argjson w "$WIDTH" --argjson h "$HEIGHT" \
        '{name:$n, prompt:$p, req_key:$r, width:$w, height:$h}')" \
      | jq '{id: .data._id, status: .data.current_status, images: .data.image_urls}'
    ;;

  nano)
    PROMPT="${2:?Usage: a2e.sh nano \"prompt\" [image_url]}"
    IMG_URL="${3:-}"
    if [[ -n "$IMG_URL" ]]; then
      BODY=$(jq -n --arg n "nano-$(date +%s)" --arg p "$PROMPT" --arg i "$IMG_URL" \
        '{name:$n, prompt:$p, input_images:[$i]}')
    else
      BODY=$(jq -n --arg n "nano-$(date +%s)" --arg p "$PROMPT" '{name:$n, prompt:$p}')
    fi
    curl -s -X POST "$BASE/api/v1/userNanoBanana/start" \
      -H "$(auth)" -H "Content-Type: application/json" -d "$BODY" \
      | jq '{id: .data._id, status: .data.current_status, images: .data.image_urls}'
    ;;

  # ── Face Swap ──────────────────────────────────────
  faceswap)
    FACE="${2:?Usage: a2e.sh faceswap <face_url> <target_video_or_image_url>}"
    TARGET="${3:?Missing target URL}"
    curl -s -X POST "$BASE/api/v1/userFaceSwapTask/add" \
      -H "$(auth)" -H "Content-Type: application/json" \
      -d "$(jq -n --arg n "fswap-$(date +%s)" --arg f "$FACE" --arg v "$TARGET" \
        '{name:$n, face_url:$f, video_url:$v}')" \
      | jq '{id: .data._id, status: .data.current_status}'
    ;;

  # ── Head Swap ──────────────────────────────────────
  headswap)
    HEAD="${2:?Usage: a2e.sh headswap <head_image_url> <target_url>}"
    TARGET="${3:?Missing target URL}"
    echo "Head Swap: endpoint TBD — check a2e.ai web UI for API updates"
    ;;

  # ── Image to Video ─────────────────────────────────
  # Models: A2E (free for max-users), Wan 2.6 Flash, Wan 2.6, Seedance 1.5 Pro, Kling 3.0
  # model_type: GENERAL (default) or FLF2V (first-last-frame, needs end_image_url)
  img2vid)
    IMG="${2:?Usage: a2e.sh img2vid <image_url> \"prompt\" [negative_prompt] [model_type] [end_image_url] [lora]}"
    PROMPT="${3:-animate this image}"
    NEG="${4:-blurry, distorted, static}"
    MODEL_TYPE="${5:-GENERAL}"
    END_IMG="${6:-}"
    LORA="${7:-}"
    BODY=$(jq -n --arg n "i2v-$(date +%s)" --arg i "$IMG" --arg p "$PROMPT" --arg np "$NEG" \
      --arg mt "$MODEL_TYPE" --arg ei "$END_IMG" --arg l "$LORA" \
      '{name:$n, image_url:$i, prompt:$p, negative_prmpt:$np, model_type:$mt}
      | if $ei != "" then . + {end_image_url:$ei} else . end
      | if $l != "" then . + {lora:$l} else . end')
    curl -s -X POST "$BASE/api/v1/userImage2Video/start" \
      -H "$(auth)" -H "Content-Type: application/json" -d "$BODY" \
      | jq '{id: .data._id, status: .data.current_status}'
    ;;

  # ── Video to Video ─────────────────────────────────
  vid2vid)
    IMG="${2:?Usage: a2e.sh vid2vid <image_url> <video_url> \"prompt\"}"
    VID="${3:?Missing video URL}"
    PROMPT="${4:-transfer motion}"
    curl -s -X POST "$BASE/api/v1/motionTransfer/start" \
      -H "$(auth)" -H "Content-Type: application/json" \
      -d "$(jq -n --arg n "v2v-$(date +%s)" --arg i "$IMG" --arg v "$VID" --arg p "$PROMPT" \
        '{name:$n, image_url:$i, video_url:$v, positive_prompt:$p, negative_prompt:\"\"}')" \
      | jq '{id: .data._id, status: .data.current_status}'
    ;;

  # ── TTS ────────────────────────────────────────────
  voices)
    curl -s -H "$(auth)" "$BASE/api/v1/anchor/voice_list" \
      | jq '[.data[] | {group: .label, voices: [.children[] | {name: .label, id: .value}]}]'
    ;;

  tts)
    TEXT="${2:?Usage: a2e.sh tts \"text\" [voice_id] [speed]}"
    VOICE="${3:-en-US-JennyNeural}"
    SPEED="${4:-1}"
    curl -s -X POST "$BASE/api/v1/video/send_tts" \
      -H "$(auth)" -H "Content-Type: application/json" \
      -d "$(jq -n --arg m "$TEXT" --arg t "$VOICE" --argjson s "$SPEED" \
        '{msg:$m, tts_id:$t, speechRate:$s}')" \
      | jq '.data'
    ;;

  # ── Voice Clone ────────────────────────────────────
  voiceclone)
    NAME="${2:?Usage: a2e.sh voiceclone \"name\" <audio_url>}"
    AUDIO="${3:?Missing audio URL}"
    MODEL="${4:-a2e}"  # a2e, cartesia, minimax, elevenlabs
    LANG="${5:-en}"
    GENDER="${6:-female}"
    curl -s -X POST "$BASE/api/v1/userVoice/training" \
      -H "$(auth)" -H "Content-Type: application/json" \
      -d "$(jq -n --arg n "$NAME" --arg a "$AUDIO" --arg m "$MODEL" --arg l "$LANG" --arg g "$GENDER" \
        '{name:$n, voice_urls:[$a], model:$m, language:$l, gender:$g}')" \
      | jq '{id: .data._id, status: .data.current_status}'
    ;;

  myvoices)
    curl -s -H "$(auth)" "$BASE/api/v1/userVoice/completedRecord" | jq '.data'
    ;;

  # ── AI Avatars ─────────────────────────────────────
  avatars)
    curl -s -H "$(auth)" "$BASE/api/v1/anchor/character_list" \
      | jq '[.data[] | {id: ._id, name: .name, type: .anchor_type}]'
    ;;

  avatar)
    ANCHOR="${2:?Usage: a2e.sh avatar <anchor_id> <audio_url> [title]}"
    AUDIO="${3:?Missing audio URL}"
    TITLE="${4:-avatar-$(date +%s)}"
    curl -s -X POST "$BASE/api/v1/video/generate" \
      -H "$(auth)" -H "Content-Type: application/json" \
      -d "$(jq -n --arg t "$TITLE" --arg a "$ANCHOR" --arg au "$AUDIO" \
        '{title:$t, anchor_id:$a, anchor_type:0, audioSrc:$au}')" \
      | jq '{id: .data._id, status: .data.current_status}'
    ;;

  # ── Talking Photo / Video ──────────────────────────
  talkphoto)
    IMG="${2:?Usage: a2e.sh talkphoto <image_url> <audio_url> [duration]}"
    AUDIO="${3:?Missing audio URL}"
    DUR="${4:-5}"
    curl -s -X POST "$BASE/api/v1/talkingPhoto/start" \
      -H "$(auth)" -H "Content-Type: application/json" \
      -d "$(jq -n --arg n "tp-$(date +%s)" --arg i "$IMG" --arg a "$AUDIO" --argjson d "$DUR" \
        '{name:$n, image_url:$i, audio_url:$a, duration:$d, prompt:\"\", negative_prompt:\"\"}')" \
      | jq '{id: .data._id, status: .data.current_status}'
    ;;

  talkvideo)
    VID="${2:?Usage: a2e.sh talkvideo <video_url> <audio_url>}"
    AUDIO="${3:?Missing audio URL}"
    curl -s -X POST "$BASE/api/v1/talkingVideo/start" \
      -H "$(auth)" -H "Content-Type: application/json" \
      -d "$(jq -n --arg n "tv-$(date +%s)" --arg v "$VID" --arg a "$AUDIO" \
        '{name:$n, video_url:$v, audio_url:$a, prompt:\"\", negative_prompt:\"\"}')" \
      | jq '{id: .data._id, status: .data.current_status}'
    ;;

  # ── AI Dubbing ─────────────────────────────────────
  dub)
    SRC="${2:?Usage: a2e.sh dub <video_url> <target_lang> [source_lang] [speakers]}"
    TLANG="${3:?Missing target language (en, de, zh, ja, es, fr, etc.)}"
    SLANG="${4:-auto}"
    SPEAKERS="${5:-1}"
    curl -s -X POST "$BASE/api/v1/userDubbing/startDubbing" \
      -H "$(auth)" -H "Content-Type: application/json" \
      -d "$(jq -n --arg n "dub-$(date +%s)" --arg s "$SRC" --arg tl "$TLANG" \
        --arg sl "$SLANG" --argjson sp "$SPEAKERS" \
        '{name:$n, source_url:$s, target_lang:$tl, source_lang:$sl, num_speakers:$sp, drop_background_audio:false}')" \
      | jq '{id: .data._id, status: .data.current_status}'
    ;;

  # ── Caption Removal ────────────────────────────────
  caption)
    VID="${2:?Usage: a2e.sh caption <video_url>}"
    curl -s -X POST "$BASE/api/v1/userCaptionRemoval/start" \
      -H "$(auth)" -H "Content-Type: application/json" \
      -d "$(jq -n --arg n "cap-$(date +%s)" --arg v "$VID" '{name:$n, video_url:$v}')" \
      | jq '{id: .data._id, status: .data.current_status}'
    ;;

  # ── Virtual Try-On ─────────────────────────────────
  tryon)
    P="${2:?Usage: a2e.sh tryon <person_url> <person_mask_url> <clothing_url> <clothing_mask_url>}"
    PM="${3:?Missing person mask URL}"
    C="${4:?Missing clothing URL}"
    CM="${5:?Missing clothing mask URL}"
    curl -s -X POST "$BASE/api/v1/virtualTryOn/start" \
      -H "$(auth)" -H "Content-Type: application/json" \
      -d "$(jq -n --arg n "tryon-$(date +%s)" --arg p "$P" --arg pm "$PM" --arg c "$C" --arg cm "$CM" \
        '{name:$n, image_urls:[$p,$pm,$c,$cm]}')" \
      | jq '{id: .data._id, status: .data.current_status}'
    ;;

  # ── Avatar Creation (Custom Twin) ────────────────────
  createavatar)
    NAME="${2:?Usage: a2e.sh createavatar \"name\" <video_or_image_url> [type]}"
    URL="${3:?Missing video or image URL}"
    TYPE="${4:-video}"  # video or image
    GENDER="${5:-female}"
    if [[ "$TYPE" == "image" ]]; then
      BODY=$(jq -n --arg n "$NAME" --arg g "$GENDER" --arg i "$URL" '{name:$n, gender:$g, image_url:$i}')
    else
      BODY=$(jq -n --arg n "$NAME" --arg g "$GENDER" --arg v "$URL" '{name:$n, gender:$g, video_url:$v}')
    fi
    curl -s -X POST "$BASE/api/v1/userVideoTwin/startTraining" \
      -H "$(auth)" -H "Content-Type: application/json" -d "$BODY" \
      | jq '{id: .data._id, status: .data.current_status}'
    ;;

  trainlipsync)
    ID="${2:?Usage: a2e.sh trainlipsync <avatar_id>}"
    curl -s -X POST "$BASE/api/v1/userVideoTwin/continueTranining" \
      -H "$(auth)" -H "Content-Type: application/json" \
      -d "$(jq -n --arg i "$ID" '{_id:$i}')" \
      | jq '{id: .data._id, status: .data.current_status}'
    ;;

  cloneavatarvoice)
    ID="${2:?Usage: a2e.sh cloneavatarvoice <avatar_id>}"
    curl -s -X POST "$BASE/api/v1/userVideoTwin/addVoiceClone" \
      -H "$(auth)" -H "Content-Type: application/json" \
      -d "$(jq -n --arg i "$ID" '{_id:$i}')" | jq '.data'
    ;;

  myavatars)
    curl -s -H "$(auth)" "$BASE/api/v1/userVideoTwin/records?pageNum=1&pageSize=10" \
      | jq '[(.data.rows // .data.list // .data // [])[] | {id: ._id, name: .name, status: .current_status}]'
    ;;

  removeavatar)
    ID="${2:?Usage: a2e.sh removeavatar <avatar_id>}"
    curl -s -X POST "$BASE/api/v1/userVideoTwin/remove" \
      -H "$(auth)" -H "Content-Type: application/json" \
      -d "$(jq -n --arg i "$ID" '{_id:$i}')" | jq '.data'
    ;;

  # ── Face Swap Image Management ─────────────────────
  addface)
    FACE="${2:?Usage: a2e.sh addface <face_image_url>}"
    curl -s -X POST "$BASE/api/v1/userFaceSwapImage/add" \
      -H "$(auth)" -H "Content-Type: application/json" \
      -d "$(jq -n --arg f "$FACE" '{face_url:$f}')" | jq '.data'
    ;;

  myfaces)
    curl -s -H "$(auth)" "$BASE/api/v1/userFaceSwapImage/records?pageNum=1&pageSize=10" \
      | jq '[(.data.rows // .data)[] | {id: ._id, url: .face_url}]'
    ;;

  delface)
    ID="${2:?Usage: a2e.sh delface <face_id>}"
    curl -s -X DELETE -H "$(auth)" "$BASE/api/v1/userFaceSwapImage/$ID" | jq '.data'
    ;;

  facepreview)
    FACE="${2:?Usage: a2e.sh facepreview <face_url> <target_url>}"
    TARGET="${3:?Missing target URL}"
    curl -s -X POST "$BASE/api/v1/userFaceSwapPreview/add" \
      -H "$(auth)" -H "Content-Type: application/json" \
      -d "$(jq -n --arg f "$FACE" --arg v "$TARGET" '{face_url:$f, video_url:$v}')" \
      | jq '{id: .data._id, status: .data.current_status}'
    ;;

  # ── Background Management ──────────────────────────
  backgrounds)
    curl -s -H "$(auth)" "$BASE/api/v1/anchor/background_list" \
      | jq '[(.data)[] | {id: ._id, url: .image_url}]'
    ;;

  addbg)
    IMG="${2:?Usage: a2e.sh addbg <image_url>}"
    curl -s -X POST "$BASE/api/v1/anchor/add_background" \
      -H "$(auth)" -H "Content-Type: application/json" \
      -d "$(jq -n --arg i "$IMG" '{image_url:$i}')" | jq '.data'
    ;;

  delbg)
    ID="${2:?Usage: a2e.sh delbg <background_id>}"
    curl -s -X DELETE -H "$(auth)" "$BASE/api/v1/anchor/background/$ID" | jq '.data'
    ;;

  # ── Product Avatar ─────────────────────────────────
  productavatar)
    echo "Product Avatar: use POST /api/v1/productAvatar/start — body TBD, check a2e.ai web UI"
    ;;

  # ── Upload & Storage ───────────────────────────────
  upload)
    URL="${2:?Usage: a2e.sh upload <url>}"
    curl -s -X POST "$BASE/api/v1/tos/transferToStorage" \
      -H "$(auth)" -H "Content-Type: application/json" \
      -d "$(jq -n --arg u "$URL" '{url:$u}')" | jq '.data'
    ;;

  presign)
    curl -s -H "$(auth)" "$BASE/api/v1/r2/get_upload_presigned_url" | jq '.data'
    ;;

  # ── Languages ──────────────────────────────────────
  languages)
    curl -s -H "$(auth)" "$BASE/api/v1/anchor/language_list?lang=en" \
      | jq '[.data[] | {code: .value, name: .label}]'
    ;;

  # ── Status / Poll (generic) ────────────────────────
  status)
    ID="${2:?Usage: a2e.sh status <id> <engine>}"
    ENGINE="${3:-t2i}"
    EP=$(engine_ep "$ENGINE")
    curl -s -H "$(auth)" "$BASE/api/v1/$EP/$ID" \
      | jq '{status: .data.current_status, result: (.data.image_urls // .data.result_url // .data.video_url), failed: .data.failed_message}'
    ;;

  poll)
    ID="${2:?Usage: a2e.sh poll <id> <engine>}"
    ENGINE="${3:-t2i}"
    EP=$(engine_ep "$ENGINE")
    while true; do
      RESULT=$(curl -s -H "$(auth)" "$BASE/api/v1/$EP/$ID")
      STATUS=$(echo "$RESULT" | jq -r '.data.current_status // "unknown"')
      echo "Status: $STATUS"
      if [[ "$STATUS" == "completed" ]]; then
        echo "$RESULT" | jq '(.data.image_urls // .data.result_url // .data.video_url)'
        break
      elif [[ "$STATUS" == "failed" ]]; then
        echo "$RESULT" | jq '{failed_code: .data.failed_code, failed_message: .data.failed_message}'
        exit 1
      fi
      sleep 12
    done
    ;;

  # ── List tasks for any engine ──────────────────────
  list)
    ENGINE="${2:-t2i}"
    EP=$(engine_ep "$ENGINE")
    curl -s -H "$(auth)" "$BASE/api/v1/$EP/allRecords?pageNum=1&pageSize=10" \
      | jq '[(.data.rows // .data.list // .data)[:5] | .[] | {id: ._id, name: .name, status: .current_status}]'
    ;;

  # ── Help ───────────────────────────────────────────
  *)
    cat <<'EOF'
a2e.sh — a2e.ai Full Platform CLI (all models FREE for max-users)

IMAGE:
  balance                              Check coin balance
  generate "prompt" [WxH] [style]      Text2Image (general|manga)
  nano "prompt" [image_url]            NanoBanana/Gemini (optional reference)

VIDEO:
  img2vid <img> "prompt" [neg] [type] [end_img] [lora]
                                       Image → video (type: GENERAL|FLF2V)
  vid2vid <img> <vid> "prompt"         Motion transfer

FACE:
  faceswap <face_url> <target_url>     Swap face onto image/video
  facepreview <face> <target>          Quick face swap preview
  headswap <head_url> <target_url>     Full head replacement (TBD)
  addface <face_image_url>             Save face for reuse
  myfaces                              List saved faces
  delface <face_id>                    Delete saved face

VOICE:
  voices                               List TTS voices
  tts "text" [voice_id] [speed]        Generate speech
  voiceclone "name" <audio_url>        Train voice clone
  myvoices                             List cloned voices
  languages                            List available languages

AVATAR:
  avatars                              List system avatars
  avatar <id> <audio_url> [title]      Generate avatar video
  createavatar "name" <url> [type]     Create custom avatar (type: video|image)
  trainlipsync <avatar_id>             Train Studio lip-sync
  cloneavatarvoice <avatar_id>         Clone voice from avatar
  myavatars                            List custom avatars
  removeavatar <avatar_id>             Delete custom avatar
  talkphoto <img> <audio> [duration]   Animate photo with audio
  talkvideo <vid> <audio>              Animate video with audio
  productavatar                        Product presentation (TBD)

BACKGROUNDS:
  backgrounds                          List avatar backgrounds
  addbg <image_url>                    Add custom background
  delbg <background_id>               Delete custom background

TOOLS:
  dub <video_url> <lang> [src] [spk]   AI Dubbing (auto voice clone)
  caption <video_url>                   Remove captions/subtitles
  tryon <person> <mask> <cloth> <cmask> Virtual Try-On
  upload <url>                          Save URL to a2e storage
  presign                               Get presigned upload URL

STATUS:
  status <id> <engine>                 Check task status
  poll <id> <engine>                   Poll until complete
  list [engine]                        List recent tasks

Engines: t2i, nano, faceswap, img2vid, vid2vid, avatar, talkphoto, talkvideo, dub, caption, tryon, voiceclone
EOF
    ;;
esac
