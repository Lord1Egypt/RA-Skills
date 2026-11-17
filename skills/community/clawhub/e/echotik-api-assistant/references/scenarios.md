# Scenario Cards

Use scenario cards to translate natural-language requests into a small, stable set of inputs.

## 1. Find creators

- User intent: "Help me find creators who are strong at commerce."
- Primary entity: creator
- Ask for:
  - product or category
  - target market
  - preferred creator size band
- Default:
  - recent time window
  - engagement-desc sort
  - exclude incomplete profiles if supported
  - use creator list when the user wants multi-filter discovery

### Creator ranking variant

- User intent: "Which creators gained the most followers recently?"
- Primary entity: creator
- Ask for:
  - market
  - time window
  - requested result size
- Default:
  - top 10
  - follower-growth-oriented sort or ranking metric
  - choose offline rank list first, then realtime detail enrichment if needed

### Creator filter variant

- User intent: "Find high-performing beauty creators in the US who are strong at commerce."
- Primary entity: creator
- Ask for:
  - target market
  - category
  - core filtering dimension
- Default:
  - use `Influencer List - EchoTik`
  - use `influencer_sort_field_v2`
  - prefer `sort_type=1`

### Creator detail variant

- User intent: "Show me this creator's profile details."
- Primary entity: creator
- Ask for:
  - `user_id` or `unique_id`
  - preferred data mode: realtime or EchoTik offline
- Default:
  - do not auto-pick mode
  - ask the user first because both offline and realtime exist

### Creator video-performance variant

- User intent: "Show me how this creator's recent videos are performing."
- Primary entity: creator
- Ask for:
  - `user_id` or `unique_id`
  - preferred data mode: realtime or EchoTik offline
- Default:
  - if the user chooses offline, prefer creator video list because it includes sales, GMV, and trend-related fields
  - if the user chooses realtime, use the realtime creator video list

### Creator trend variant

- User intent: "Show me this creator's follower-growth trend over the last 180 days."
- Primary entity: creator
- Ask for:
  - `user_id`
  - time range
- Default:
  - prefer `Influencer Trend Snapshot - EchoTik`
  - explain that missing dates usually mean no metric change on those days

## 2. Find winning products

- User intent: "What products are breaking out right now?"
- Primary entity: product
- Ask for:
  - category
  - market
  - time range
- Default:
  - growth-desc sort
  - minimum activity threshold
  - `off_mark=0`
  - resolve category names through the category-list APIs before calling category-sensitive product endpoints

### Product leaderboard variant

- User intent: "What are the top 10 best-selling products in the US this week?"
- Primary entity: product
- Ask for:
  - market
  - time window
  - requested result size
- Default:
  - top 10
  - prefer `Product Rank List - EchoTik`
  - treat date alignment as a T+1 periodic leaderboard rule

### Product detail variant

- User intent: "Show me this product's details."
- Primary entity: product
- Ask for:
  - `product_id` or product share link
  - preferred data mode: realtime or EchoTik offline
  - region if realtime is chosen
- Default:
  - if the input is a share link, resolve `product_id` first
  - do not auto-pick mode
  - ask the user first because offline and realtime detail flows both exist

### Product comments variant

- User intent: "Show me the comments for this product."
- Primary entity: product
- Ask for:
  - `product_id` or product share link
  - preferred data mode: realtime or EchoTik offline
  - region if realtime is chosen
- Default:
  - if the input is a share link, resolve `product_id` first
  - ask the user to choose between offline collected comments and realtime comments
  - if realtime is chosen, paginate from `offset=1` and follow `next_cursor`

## 3. Analyze a shop

- User intent: "Help me assess whether this shop is worth researching."
- Primary entity: shop
- Ask for:
  - shop link or shop name
  - market
- Default:
  - recent 30-day window
  - resolve category names through the seller-category APIs before calling category-sensitive seller endpoints

### Shop leaderboard variant

- User intent: "What are the top cross-border shops in this market?"
- Primary entity: shop
- Ask for:
  - market
  - time window
  - local versus cross-border preference
- Default:
  - prefer `Seller Rank List - EchoTik`
  - apply the same periodic date logic used by the product leaderboard family

### Shop detail variant

- User intent: "Show me this shop's details."
- Primary entity: shop
- Ask for:
  - `seller_id`
- Default:
  - prefer `Seller Detail - EchoTik`
  - if offline detail is empty, explain that the shop may not be collected in EchoTik offline data

### Shop product-list variant

- User intent: "Show me this shop's products."
- Primary entity: shop
- Ask for:
  - `seller_id`
  - preferred data mode: realtime or EchoTik offline
  - region if realtime is chosen
- Default:
  - do not auto-pick mode
  - ask the user first because offline and realtime seller product-list flows differ

## 4. Analyze a video

- User intent: "Why did this video perform so well?"
- Primary entity: video
- Ask for:
  - video link or `video_id`
- Default:
  - return creator and product context if available
  - prefer realtime 14-day interaction trend over offline trend snapshots when the user asks for recent video trend performance

### Video discovery variant

- User intent: "Find AI commerce videos in this market."
- Primary entity: video
- Ask for:
  - market
  - category if relevant
  - core filter such as AI, commerce, or ad
- Default:
  - prefer `Video List - EchoTik`
  - if category semantics are needed, resolve category IDs through the product-category APIs first

### Video leaderboard variant

- User intent: "What are the top-selling videos in this category this week?"
- Primary entity: video
- Ask for:
  - market
  - category
  - time window
- Default:
  - prefer `Video Rank List - EchoTik`
  - use the same periodic date logic used by the other leaderboard families

### Video detail variant

- User intent: "Show me this video's details."
- Primary entity: video
- Ask for:
  - `video_id`
  - preferred data mode: realtime or EchoTik offline
- Default:
  - do not auto-pick mode
  - ask the user first because offline and realtime video detail both exist
  - if offline detail is empty, fall back to realtime detail

### Hashtag video variant

- User intent: "Show me videos related to this hashtag."
- Primary entity: hashtag
- Ask for:
  - `hashtag_id` or hashtag text
- Default:
  - if only hashtag text is known, resolve `hashtag_id` through hashtag search first
  - then fetch the hashtag's related video list

## 5. Compare competitors

- User intent: "Compare these brands, shops, or creators."
- Primary entity: mixed
- Ask for:
  - comparison targets
  - market
  - time range
- Default:
  - normalize by the same date range

## 6. Search across entities

- User intent: "Search creators, products, videos, hashtags, music, or live sessions."
- Primary entity: search target
- Ask for:
  - keyword or image input
  - target entity
  - market if relevant
- Default:
  - prefer the dedicated realtime search endpoint for that entity
  - use universal EchoTik search only as a fallback
  - if the user searches by product image, run photo search first and then photo-search pagination for more results

## 7. Analyze live sessions

- User intent: "Show me this live room's detail."
- Primary entity: live room
- Ask for:
  - `room_id`
  - `user_id`
- Default:
  - prefer realtime live detail
  - explain that it only works while the room is currently live

## 8. Advanced mode

Use this only when the user explicitly wants fine-grained control.

- Show grouped filters rather than the full raw schema.
- Order filters as:
  - required
  - recommended
  - advanced

## 9. Comprehensive report mode

Use this when the user explicitly asks for a full report on a creator, product, or seller.

- Confirm which related sections should be included before running every adjacent endpoint family.
- Typical creator-report sections:
  - detail
  - trend
  - followers
  - following
  - videos
  - live history
  - promoted products
  - region
  - milestones
- Typical product-report sections:
  - detail
  - trend
  - comments
  - related creators
  - related videos
  - related live sessions
  - leaderboard context
- Typical seller-report sections:
  - detail
  - trend
  - product inventory
  - related creators
  - related videos
  - related live sessions
  - leaderboard context
- If the user only wants the most important sections, do not call every related endpoint by default.
