# Facebook use cases via Agiexa

Example prompts a merchant will be able to give their agent after Agiexa launches (November 2026). They are illustrations of future use - do not run them today.

More examples and live demos: https://agiexa.com/integrations/facebook

## Turn Facebook Engagement Into Product Ideas

Analyze your best-performing Facebook posts and connect audience engagement with relevant Shopify products to discover what deserves more attention.

- Apps: Facebook, Shopify
- Tools: `FACEBOOK_GET_PAGE_POSTS`, `FACEBOOK_GET_POST_INSIGHTS`, `FACEBOOK_GET_PAGE_INSIGHTS`

> Act as my Facebook and Shopify marketing analyst. Review my recent Facebook Page posts, reaction counts, and available post insights. Identify the posts that perform best based on the available engagement data. Where possible, match product-related posts to products in my Shopify catalog. Summarize which products attract the most engagement, explain what the data actually supports, and suggest five content ideas for products worth promoting next. Distinguish engagement from actual sales and do not claim that a post generated revenue unless the necessary sales attribution data is available.

## Create Product Posts From Shopify Catalog

Turn Shopify product information into engaging Facebook posts featuring accurate prices, product details, images, and shopping links.

- Apps: Facebook, Shopify
- Tools: `FACEBOOK_CREATE_POST`, `FACEBOOK_CREATE_PHOTO_POST`

> Act as my Facebook content creator for my Shopify store. When I provide a product or collection, retrieve the relevant Shopify product details, including its title, price, description, and available images. Draft an engaging Facebook post tailored to the product and its intended audience. Include a natural call to action and the product URL when available. Never invent product features, prices, discounts, or availability. Show me the complete post and proposed images for approval before publishing anything to my Facebook Page.

## Answer Facebook Product Questions Automatically

Use Shopify product information to help answer Facebook messages about pricing, product details, and availability accurately.

- Apps: Facebook, Shopify
- Tools: `FACEBOOK_GET_PAGE_CONVERSATIONS`, `FACEBOOK_GET_CONVERSATION_MESSAGES`, `FACEBOOK_SEND_MESSAGE`

> Act as my Facebook customer support assistant for my Shopify store. Review Facebook Page conversations and identify customer messages asking about product prices, product details, or stock availability. Match each question to the correct Shopify product where possible and retrieve the relevant information. Draft a concise, friendly, personalized response using verified product data. If a product match is ambiguous or information is unavailable, ask me for clarification. Do not invent prices, promise availability, or send customer messages without my approval.

## Discover Popular Products From Social Engagement

Combine Facebook post performance with Shopify product information to identify products that may deserve additional marketing attention.

- Apps: Facebook, Shopify
- Tools: `FACEBOOK_GET_POST_INSIGHTS`, `FACEBOOK_GET_PAGE_POSTS`

> Act as my social commerce analyst. Review Facebook Page posts and their available insights, then match product-related posts to the corresponding Shopify products. Create a ranked list based on relevant engagement metrics, product relevance, and verified inventory availability. Include the post, associated product, engagement observations, current price where available, and recommended next marketing action. Clearly explain the ranking criteria and data limitations. Do not assume that likes or reactions directly translate into purchases, and do not recommend promoting unavailable products without flagging the stock issue.

## Publish Engaging Multi-Photo Product Posts

Create visually appealing Facebook posts using multiple product photos and compelling copy to encourage shoppers to explore your Shopify products.

- Apps: Facebook, Shopify
- Tools: `FACEBOOK_CREATE_MULTI_PHOTO_POST`, `FACEBOOK_UPLOAD_PHOTOS_BATCH`

> Act as my Facebook product marketing assistant. When I select a Shopify product, retrieve its relevant product information and available images. Draft an engaging Facebook post designed for a multi-photo format, with a compelling opening, concise product benefits, a natural call to action, and a link to the product. Select suitable public image URLs when available and ensure that the images actually represent the selected product. If suitable images are unavailable, ask me to provide them. Show me the final copy and image selection for approval before publishing the post.

## Investigate Negative Feedback and Comments

Review Facebook comments and engagement to identify customer concerns, recurring complaints, and opportunities to improve products or customer support.

- Apps: Facebook, Shopify
- Tools: `FACEBOOK_GET_COMMENTS`, `FACEBOOK_CREATE_COMMENT`

> Act as my Facebook customer feedback analyst. Review comments on my recent Facebook Page posts and identify questions, complaints, product concerns, and positive feedback. Where relevant, connect customer feedback to products in my Shopify catalog. Group the findings by topic and urgency, summarize recurring issues, and suggest appropriate responses or operational improvements. Draft replies for my review. Do not delete comments, publish replies, or make changes to product information without my explicit approval. Distinguish actual customer feedback from your own interpretation.

## Turn Customer Messages Into Shopify Actions

Connect Facebook customer conversations with Shopify orders and product information to help resolve inquiries more efficiently.

- Apps: Facebook, Shopify
- Tools: `FACEBOOK_GET_PAGE_CONVERSATIONS`, `FACEBOOK_GET_CONVERSATION_MESSAGES`, `FACEBOOK_SEND_MESSAGE`

> Act as my Facebook and Shopify customer operations assistant. Review relevant Facebook Page conversations and identify messages that may require checking a Shopify product, order, or inventory record. When the customer provides an order number or sufficient identifying information, retrieve the corresponding Shopify information where permitted. Summarize the customer's issue, the relevant order or product details, and the recommended next step. Draft a clear customer response using verified information. Do not expose another customer's information, guess order matches, issue refunds, cancel orders, or change records without my approval.

## Keep Facebook Promotions Accurate

Prepare Facebook promotional posts using current Shopify product prices, availability, and approved discounts to avoid misleading shoppers.

- Apps: Facebook, Shopify
- Tools: `FACEBOOK_CREATE_POST`, `FACEBOOK_UPDATE_POST`

> Act as my Facebook promotions assistant. Before drafting a promotional post, verify the selected Shopify product's current price, available stock, and any discount details I provide. Prepare clear, engaging copy with accurate promotional terms and a relevant product link. If the promotion has a deadline, minimum purchase requirement, or eligibility restriction, include it accurately. Flag any missing or conflicting information before proceeding. Show me the final post for approval and publish it only after I confirm. Never invent discounts, create unapproved offers, or advertise unverified stock availability.

## Improve Content Using Customer Conversations

Use recurring Facebook messages and comments to identify gaps in product descriptions and create more relevant content for your Shopify store.

- Apps: Facebook, Shopify
- Tools: `FACEBOOK_GET_PAGE_CONVERSATIONS`, `FACEBOOK_GET_COMMENTS`

> Act as my Facebook audience insights assistant. Analyze available Facebook comments and Page conversations to identify recurring questions about my Shopify products, such as sizing, materials, pricing, availability, usage, and shipping. Connect those questions to the relevant products where possible. Summarize the most frequent themes and recommend improvements to product descriptions, frequently asked questions, and future Facebook posts. Draft suggested content using verified information only. Do not update Shopify pages, publish Facebook content, or send messages without my approval.

## Generate Weekly Facebook and Shopify Reports

Combine Facebook engagement insights with Shopify catalog and order information to produce a practical weekly marketing report.

- Apps: Facebook, Shopify
- Tools: `FACEBOOK_GET_PAGE_INSIGHTS`, `FACEBOOK_GET_POST_INSIGHTS`, `FACEBOOK_GET_PAGE_POSTS`

> Act as my weekly Facebook and Shopify marketing analyst. For the specified date range, review available Facebook Page insights, post performance, reactions, comments, and relevant customer conversations. Retrieve corresponding Shopify product information and order data where available. Summarize top-performing posts, recurring customer questions, products receiving attention, inventory concerns affecting promotions, and recommended content for the next week. Include actual metrics only when supported by the retrieved data. Clearly distinguish engagement metrics from orders, sales, and conversion rates. Do not claim that Facebook content generated Shopify sales unless the necessary attribution data is available. Finish with five prioritized recommendations for my next marketing cycle.
