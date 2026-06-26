# Credential Guides — Finding Your Ad Platform API Keys

Use these guides when a user doesn't know where to find their credentials.
Explain each step warmly and simply.

---

## Meta (Facebook & Instagram Ads)

You need two things: your **Ad Account ID** and an **Access Token**.

### Ad Account ID
1. Go to [business.facebook.com](https://business.facebook.com)
2. Click **Ad Accounts** in the left sidebar
3. Your Ad Account ID is shown — it looks like `act_1234567890`

### Access Token
1. Go to [developers.facebook.com](https://developers.facebook.com)
2. Click **My Apps** → **Create App** → choose **Business** type
3. Add the **Marketing API** product to your app
4. Go to **Tools** → **Graph API Explorer**
5. Select your app and click **Generate Access Token**
6. Select these permissions: `ads_management`, `ads_read`, `business_management`
7. Copy the token shown

> ⚠️ For a long-lived token (doesn't expire every hour), exchange your short-lived token:
> `GET https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id={app_id}&client_secret={app_secret}&fb_exchange_token={short_token}`

---

## Google Ads

Google Ads API requires more setup than others. You'll need:
- **Developer Token** (from your Google Ads Manager account)
- **Customer ID** (your Google Ads account number, like `123-456-7890`)
- **OAuth2 credentials** (Client ID, Client Secret, Refresh Token)

### Developer Token
1. Sign in to your [Google Ads Manager account](https://ads.google.com)
2. Go to **Tools & Settings** → **API Center**
3. Apply for API access — basic access is usually approved quickly
4. Copy your **Developer Token**

### OAuth2 Credentials
1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project (or use an existing one)
3. Enable the **Google Ads API**
4. Go to **APIs & Services** → **Credentials** → **Create Credentials** → **OAuth 2.0 Client IDs**
5. Choose **Desktop app**, download the JSON file
6. Use Google's OAuth Playground or the Python client library to exchange for a **Refresh Token**

> 💡 This is more technical than other platforms. Consider using [Google's OAuth2 Playground](https://developers.google.com/oauthplayground/) to get your refresh token.

---

## X (Twitter) Ads

1. Go to [developer.twitter.com](https://developer.twitter.com)
2. Apply for a developer account (standard access is usually approved within 1–2 days)
3. Create a new Project and App
4. Under your App settings, go to **Keys and Tokens**
5. Generate your **API Key**, **API Secret**, **Access Token**, and **Access Token Secret**
6. Make sure your app has **Read and Write** permissions enabled
7. Your **Ad Account ID** is found at [ads.twitter.com](https://ads.twitter.com) → click your account name at the top

> ⚠️ X Ads API requires a **Funding Instrument** (credit card) to be set up via ads.twitter.com before you can create campaigns via the API. Funding instruments cannot be created through the API.

---

## Snapchat Ads

1. Go to [developers.snap.com](https://developers.snap.com)
2. Click **Create App** in the Business section
3. Fill in your app details and submit for review
4. Once approved, go to your app settings and copy your **Client ID** and **Client Secret**
5. Follow Snapchat's OAuth2 flow to get a **Refresh Token**:
   - Authorization URL: `https://accounts.snapchat.com/login/oauth2/authorize`
   - Token URL: `https://accounts.snapchat.com/login/oauth2/access_token`
6. Your **Ad Account ID** is found in [Snapchat Ads Manager](https://ads.snapchat.com) → your account settings

> 💡 Snapchat's API access requires an approved application. The review process usually takes 1–3 business days.
