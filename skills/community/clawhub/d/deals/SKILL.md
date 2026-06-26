name: tome.deals.global

display:  ToMe Global Deals

description: >

&#x20; Global daily deal curation on ToMe Marketplace.

&#x20; Always 3 results: top save, trending, personalized.

brand: ToMe Digital Service Marketplace



safety:

&#x20; read\_only: true

&#x20; public\_only: true

&#x20; respect\_robots: true

&#x20; gentle\_rate\_limit: true

&#x20; no\_login: true

&#x20; no\_form\_submit: true

&#x20; compliant\_api\_friendly: true



sources:

&#x20; # North America

&#x20; - dealmoon.com

&#x20; - dealnews.com

&#x20; - dealcatcher.com

&#x20; - retailmenot.com

&#x20; - redflagdeals.com

&#x20; - woot.com



&#x20; # Europe

&#x20; - hotukdeals.com

&#x20; - mydealz.de

&#x20; - dealabs.com

&#x20; - promodescuentos.com

&#x20; - pepper.ru

&#x20; - pepper.pl

&#x20; - ibood.com

&#x20; - yakala.co



&#x20; # Asia Pacific

&#x20; - ozbargain.com.au

&#x20; - kakaku.com

&#x20; - pelando.com.br

&#x20; - fmkorea.com



&#x20; # Gaming \& Virtual Products

&#x20; - cheapshark.com

&#x20; - isthereanydeal.com

&#x20; - gg.deals

&#x20; - humblebundle.com

&#x20; - fanatical.com

&#x20; - greenmangaming.com

&#x20; - gog.com



output:

&#x20; count: 3

&#x20; structure:

&#x20;   - label: Best Savings

&#x20;     fields: \[ title, description, price, discount, url ]

&#x20;   - label: Trending Now

&#x20;     fields: \[ title, description, price, heat, url ]

&#x20;   - label: For You

&#x20;     fields: \[ title, description, price, match\_reason, url ]

&#x20; refresh:

&#x20;   allowed: true

&#x20;   max\_per\_session: 5



intents:

&#x20; - Show today's global deals

&#x20; - Get top discounts worldwide

&#x20; - Refresh my deal picks

&#x20; - Show more deals

&#x20; - Find gaming deals

