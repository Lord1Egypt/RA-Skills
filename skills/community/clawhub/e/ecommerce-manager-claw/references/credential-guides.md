# Credential Guides — Where to Find Your API Keys

Use these step-by-step guides when the user isn't sure where to find their credentials.
Explain each step in plain, friendly language.

---

## Shopify

1. Log in to your Shopify admin panel
2. Go to **Settings** → **Apps and sales channels** → **Develop apps**
3. Click **Create an app**, give it a name (e.g. "Claude Assistant")
4. Under **Configuration**, enable the Admin API scopes you need:
   - `read_products`, `write_products` — for product management
   - `read_orders`, `write_orders` — for order management
   - `read_inventory`, `write_inventory` — for inventory
   - `read_customers`, `write_customers` — for customers
5. Click **Install app**, then copy the **Admin API access token**
6. Your store URL is `yourstore.myshopify.com`

---

## WooCommerce

1. Log in to your WordPress admin dashboard
2. Go to **WooCommerce** → **Settings** → **Advanced** → **REST API**
3. Click **Add key**
4. Set Description (e.g. "Claude"), User, and Permissions to **Read/Write**
5. Click **Generate API key**
6. Copy the **Consumer Key** and **Consumer Secret** shown (you won't see them again!)
7. Your site URL is your WordPress website address

---

## BigCommerce

1. Log in to your BigCommerce control panel
2. Go to **Settings** → **API** → **API Accounts**
3. Click **Create API Account** → **Create V2/V3 API Token**
4. Set a name and select permissions for Products, Orders, Customers, Inventory
5. Click **Save** and copy the **Access Token**
6. Your Store Hash is in the URL: `store-XXXXXXX.mybigcommerce.com`

---

## Wix

1. Go to [manage.wix.com](https://manage.wix.com)
2. Select your site → **Settings** → **Developer Tools** → **API Keys**
3. Click **Generate API Key**
4. Select the permissions (Stores, Orders, etc.)
5. Copy the **API Key**
6. Your Site ID is found under **Settings** → **General Info** → **Site ID**

---

## PrestaShop

1. Log in to your PrestaShop back office
2. Go to **Advanced Parameters** → **Web Service**
3. Click **Add new webservice key**
4. Set permissions (GET, PUT, POST, DELETE) for resources you need
5. Copy the generated **API Key**
6. Your store URL is your PrestaShop website address

---

## Adobe Commerce / Magento

1. Log in to your Magento Admin
2. Go to **System** → **Integrations** → **Add New Integration**
3. Fill in the name, then go to **API** tab and select resource access
4. Click **Save** → **Activate** → **Allow**
5. Copy the **Access Token**
6. Your store URL is your Magento website address

---

## Amazon SP-API

This is more complex — recommend the user contact their developer or refer to:
https://developer-docs.amazon.com/sp-api/docs/getting-started

Key items needed:
- **Marketplace ID** (e.g. ATVPDKIKX0DER for US)
- **LWA Client ID** and **Client Secret** (from Seller Central → App Console)
- **Refresh Token** (generated during OAuth flow)

---

## Etsy

1. Go to [etsy.com/developers](https://www.etsy.com/developers)
2. Click **Create a New App**
3. Fill in app details, select **Read** and **Write** scopes
4. Follow the OAuth2 flow to get an **Access Token**
5. Your **Shop ID** is found in your Etsy shop URL

---

## Shopware

1. Log in to your Shopware Admin
2. Go to **Settings** → **System** → **Integrations**
3. Click **Add integration**
4. Enable **Administrator** role or set custom permissions
5. Copy the **Access Key ID** and **Secret Access Key**
6. Your store URL is your Shopware website address
