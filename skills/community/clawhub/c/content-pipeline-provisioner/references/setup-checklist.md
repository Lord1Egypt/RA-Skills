# Setup Checklist — Content Pipeline Provisioner

Complete each section before running "provision pipeline". Takes ~30 minutes total.

---

## 0. Required Skills (install these first)

This skill runs on top of two other tools. Install both before anything else.

**Larry (TikTok posting engine)**
- Download from larrybrain.com or run: `clawhub install larry`
- Drop the skill folder into your OpenClaw skills directory
- Larry handles TikTok image generation, hook packs, slide assembly, and Postiz scheduling
- This skill configures and orchestrates Larry — it does not replace it

**OpenClaw**
- Required to run this skill at all
- Download at openclaw.ai if you haven’t already

---

## 1. Postiz (TikTok + Twitter scheduling)
1. Create account at postiz.com (free plan works for 1 channel, paid for multiple)
2. Connect your TikTok account: Postiz dashboard → Channels → Add Channel → TikTok
3. Connect your Twitter/X account: Postiz dashboard → Channels → Add Channel → Twitter
4. Get your API key: Postiz dashboard → Settings → API → Copy API key
5. Get your integration IDs: After connecting channels, each channel has an ID visible in the URL or API response
6. Save to your config: postiz.apiKey + postiz.integrationIds.tiktok + postiz.integrationIds.twitter

## 2. Twitter/X API (direct posting — optional if using Postiz only)
1. Apply at developer.twitter.com
2. Basic tier required for posting ($100/mo) — OR use Postiz OAuth only (free, no direct API needed)
3. If using direct API: save API key, secret, access token, access secret to ~/.openclaw/.env

## 3. MailerLite (newsletter)
1. Create account at mailerlite.com (free up to 1,000 subscribers)
2. Create a subscriber group for your audience
3. Get API key: MailerLite dashboard → Integrations → API → Generate token
4. Get your group ID: Groups page → click your group → ID is in the URL
5. Save to newsletter-writer/config.json: mailerLiteSecretFile + groupId

## 4. Telegram (briefings)
1. Message @BotFather on Telegram → /newbot → follow prompts
2. Save the bot token
3. Get your chat ID: message your bot, then fetch https://api.telegram.org/bot{TOKEN}/getUpdates
4. Save TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID to ~/.openclaw/.env

## 5. OpenAI API (image generation for TikTok slides)
1. Get API key at platform.openai.com
2. Save OPENAI_API_KEY to ~/.openclaw/.env
3. Note: gpt-image-1.5 costs ~$0.04/image. ~30 images/month = ~$1.20/month per pipeline

## 6. Supabase + Netlify (blog publishing)
1. Create Supabase project at supabase.com
2. Create blog_articles table — schema at references/blog-schema.md
3. Get service role key: Supabase → Settings → API → service_role key
4. Create Netlify site (or connect existing) and get deploy hook URL
5. Save SUPABASE_URL + SUPABASE_SERVICE_KEY + NETLIFY_DEPLOY_HOOK to ~/.openclaw/.env
6. Note: Blog publishing requires your site to be connected to Supabase — see references/blog-schema.md

## 7. Verify everything
Run: `node scripts/verify-setup.js` (coming soon — manual check for now)
Confirm each credential is in ~/.openclaw/.env or the relevant config file.

---

## Estimated Monthly API Costs

| Service | Cost |
|---|---|
| OpenAI (images) | ~$1-3/month |
| OpenAI (text generation) | ~$2-5/month |
| Postiz | Free (1 channel) or $29/mo (multiple) |
| MailerLite | Free up to 1K subscribers |
| Supabase | Free tier (generous) |
| Netlify | Free tier |
| **Total** | **~$3-8/month** |
