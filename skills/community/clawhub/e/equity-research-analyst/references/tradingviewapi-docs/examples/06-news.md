# News

- Source: `openapi.json`
- Generated At: `2026-04-21T18:58:33+08:00`
- Live Requests: `enabled`

## Get News List

`GET /api/news`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/api/news?symbol=NASDAQ%3AAAPL&lang=en&market=stock&market_country=US' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "tag:reuters.com,2026:newsml_L1N41401E:0",
        "title": "Apple's new CEO is a product perfectionist taking on the AI age",
        "published": 1776765600,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L1N41401E:0-apple-s-new-ceo-is-a-product-perfectionist-taking-on-the-ai-age/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260421001775:0",
        "title": "Tim Cook Told Me His Advice for Apple's Next CEO — WSJ",
        "published": 1776763800,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260421001775:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260421001551:0",
        "title": "How Apple Stock Has Fared Under Tim Cook — WSJ",
        "published": 1776761940,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260421001551:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260421001485:0",
        "title": "Apple AI Ambitions Helped by Incoming CEO's Hardware Experience — Market Talk",
        "published": 1776760800,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260421001485:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:9cafd3a72094b:0",
        "title": "Nasdaq, S&P 500 Futures Steady As Iran Talks, Warsh Hearing Set Market Tone: Why AAPL, AMZN, POET, FRMI, IBRX Are In Focus",
        "published": 1776760781,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/nasdaq-sp500-futures-rise-aapl-amzn-poet-frmi-ibrx-stocks-to-watch/cZBIfgmRICh",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "BCBA:SPY",
            "logoid": "spdr-sandp500-etf-tr"
          }
        ],
        "storyPath": "/news/stocktwits:9cafd3a72094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_DN20260420009243:0",
        "title": "Apple CEO Cook Plans His Departure. The Tech Giant He Leaves Behind Won't Be the Same. — Barrons.com",
        "published": 1776759180,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260420009243:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:5692ebe19094b:0",
        "title": "Apple's New CEO Led A Silicon 'Brain Transplant' — Analyst Says That's Exactly Why John Ternus Is Right For Next AI Phase",
        "published": 1776757050,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-s-new-ceo-led-a-silicon-brain-transplant-analyst-says-that-s-exactly-why-john-ternus-is-right-for-next-ai-phase/cZBI9pwRICa",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:5692ebe19094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "tradingview:d76fed67f094b:0",
        "title": "AAPL: Apple Stock Tumbles as CEO Tim Cook Announces Departure After 15 Years",
        "published": 1776755710,
        "urgency": 2,
        "link": "https://www.tradingview.com",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/tradingview:d76fed67f094b:0-aapl-apple-stock-tumbles-as-ceo-tim-cook-announces-departure-after-15-years/",
        "provider": {
          "id": "tradingview",
          "name": "TradingView",
          "logo_id": "tradingview-snaps"
        }
      },
      {
        "id": "sharecast:674e9b6e8094b:0",
        "title": " Apple names John Ternus as CEO to replace Tim Cook ",
        "published": 1776753179,
        "urgency": 2,
        "link": "https://www.sharecast.com/news/news-and-announcements/apple-names-john-ternus-as-ceo-to-replace-tim-cook--22320629.html",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/sharecast:674e9b6e8094b:0/",
        "provider": {
          "id": "sharecast",
          "name": "ShareCast",
          "logo_id": "sharecast"
        }
      },
      {
        "id": "stocktwits:99c909d7b094b:0",
        "title": "Apple After Tim Cook: Analysts See Continuity Pick, Not Vision Play Under New CEO John Ternus",
        "published": 1776740903,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-after-tim-cook-analysts-see-continuity-pick-not-vision-play-under-new-ceo-john-ternus/cZBIPluRIzz",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:99c909d7b094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_DN20260420009691:0",
        "title": "The Rise of Apple's New CEO: A Hardware Expert Takes Over in the AI Era — WSJ",
        "published": 1776739500,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260420009691:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L6N41400X:0",
        "title": "Apple CEO’s best bet: channel both Jobs and Cook",
        "published": 1776733042,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L6N41400X:0-apple-ceo-s-best-bet-channel-both-jobs-and-cook/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_SN20260420010143:0",
        "title": "Apple CEO Tim Cook to step down after overseeing 1,900% stock surge. His successor faces big challenges.",
        "published": 1776732180,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_SN20260420010143:0/",
        "provider": {
          "id": "market-watch",
          "name": "MarketWatch",
          "logo_id": "marketwatch"
        }
      },
      {
        "id": "DJN_DN20260420008139:0",
        "title": "Tim Cook to Step Down as Apple Names New CEO — WSJ",
        "published": 1776730980,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260420008139:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "dpa_afx:d24ca8bee7549:0",
        "title": "Apple Names John Ternus CEO; Tim Cook To Become Executive Chairman",
        "published": 1776723693,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/dpa_afx:d24ca8bee7549:0-apple-names-john-ternus-ceo-tim-cook-to-become-executive-chairman/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L4N4131HC:0",
        "title": "Who is John Ternus, Apple's new CEO?",
        "published": 1776721816,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L4N4131HC:0-who-is-john-ternus-apple-s-new-ceo/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260420008672:0",
        "title": "Apple's New CEO Will Face Immediate Pressure on AI Strategy — Market Talk",
        "published": 1776721080,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260420008672:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tradingview:9a9b700e6fc12:0",
        "title": "Apple's Tim Cook to Become Executive Chair; John Ternus Named CEO",
        "published": 1776720780,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/tradingview:9a9b700e6fc12:0-apple-s-tim-cook-to-become-executive-chair-john-ternus-named-ceo/",
        "provider": {
          "id": "tradingview",
          "name": "TradingView",
          "logo_id": "tradingview-snaps"
        }
      },
      {
        "id": "DJN_DN20260420008527:0",
        "title": "Apple's CEO Change Timing Will Garner Mixed Reaction, Analyst Says — Market Talk",
        "published": 1776720240,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260420008527:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260420008407:0",
        "title": "Apple Stock Down After-Hours After John Ternus Named Next CEO — WSJ",
        "published": 1776719280,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260420008407:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260420008355:0",
        "title": "Apple Picks Exec With Core Hardware Expertise as Next CEO — Market Talk",
        "published": 1776719040,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260420008355:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260420008272:0",
        "title": "Apple's Cook to Continue to Engage With Global Policymakers — Market Talk",
        "published": 1776718620,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260420008272:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:0acb0ab69094b:0",
        "title": "Apple Appoints New CEO; Tim Cook Shifts To Executive Chairman",
        "published": 1776718532,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-appoints-new-ceo-tim-cook-shifts-to-executive-chairman/cZBdnvoRIzq",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:0acb0ab69094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_DN20260420008241:0",
        "title": "Apple's Ends Months of Speculation Over Tim Cook's Successor — Market Talk",
        "published": 1776718500,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260420008241:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L4N4131GO:0",
        "title": "Apple turns to hardware veteran Ternus as CEO to succeed Cook in AI age",
        "published": 1776717647,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L4N4131GO:0-apple-turns-to-hardware-veteran-ternus-as-ceo-to-succeed-cook-in-ai-age/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN4130WL:0",
        "title": "Johny Srouji Named Apple’s Chief Hardware Officer",
        "published": 1776717291,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN4130WL:0-johny-srouji-named-apple-s-chief-hardware-officer/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L4N4131GB:0",
        "title": "John Ternus to become Apple CEO, Tim Cook to become executive chairman",
        "published": 1776717225,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L4N4131GB:0-john-ternus-to-become-apple-ceo-tim-cook-to-become-executive-chairman/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260420007764_20260420007925:0",
        "title": "Apple: Ternus Will Join the Bd of Directors, Also Effective Sept 1 >AAPL",
        "published": 1776717180,
        "urgency": 1,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260420007764_20260420007925:0/",
        "is_flash": true,
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260420007764_20260420007885:0",
        "title": "Apple: Transition, Which Was Approved Unanimously by the Bd of Directors, Follows a Thoughtful, Long-Term Succession Planning Process >AAPL",
        "published": 1776717060,
        "urgency": 1,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260420007764_20260420007885:0/",
        "is_flash": true,
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260420007788_20260420007857:0",
        "title": "Apple: Johny Srouji Will Become Chief Hardware Officer, Effective Immediately >AAPL",
        "published": 1776717000,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260420007788_20260420007857:0/",
        "is_flash": true,
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260420006199:0",
        "title": "Apple Stock Can Hit $300 Despite Memory Headwinds, Analyst Says. Here's How. — Barrons.com",
        "published": 1776703320,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260420006199:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260418000740:0",
        "title": "Berkshire May Have Sold $15 Billion of Stocks Run by Former Manager — Barrons.com",
        "published": 1776527760,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NYSE:AXP",
            "logoid": "american-express"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:BRK.A",
            "logoid": "berkshire-hathaway"
          },
          {
            "symbol": "NYSE:COF",
            "logoid": "capital-one"
          },
          {
            "symbol": "NYSE:OXY",
            "logoid": "occidental-petroleum"
          }
        ],
        "storyPath": "/news/DJN_DN20260418000740:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:5dd968a69094b:0",
        "title": "Apple Clears Major Legal Hurdle After US Trade Tribunal Shuts Down Masimo’s Latest Watch Ban Attempt",
        "published": 1776472317,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-clears-major-legal-hurdle-after-us-trade-tribunal-shuts-down-masimos-latest-watch-ban-attempt/cZJ6WUSRIUr",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:5dd968a69094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L6N4101BB:0",
        "title": "Apple defeats bid for new Apple Watch import ban at US trade tribunal ",
        "published": 1776467696,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MASI",
            "logoid": "masimo"
          },
          {
            "symbol": "NYSE:DHR",
            "logoid": "danaher"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L6N4101BB:0-apple-defeats-bid-for-new-apple-watch-import-ban-at-us-trade-tribunal/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260417004938:0",
        "title": "Apple Seen Poised to Gain Smartphone Market Share — Market Talk",
        "published": 1776441060,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260417004938:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:abfd331bf094b:0",
        "title": "Apple’s China Surge Shows Pricing Power Matters In A Supply Crunch – Retail Bulls Take Notice",
        "published": 1776435624,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-china-surge-shows-pricing-power-matters-in-a-supply-crunch-retail-bulls-take-notice/cZJUsxBRIUG",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:abfd331bf094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_DN20260417004032:0",
        "title": "Apple Raised to Outperform From Neutral by BNP Paribas",
        "published": 1776434400,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260417004032:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L1N41008E:0",
        "title": "Apple's iPhone shipments in China surge 20% in Q1, data shows",
        "published": 1776414427,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "HKEX:1810",
            "logoid": "xiaomi"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L1N41008E:0-apple-s-iphone-shipments-in-china-surge-20-in-q1-data-shows/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L4N4100B5:0",
        "title": "Apple marketing chief for watch, AirPods, home and health Stan Ng retires - Bloomberg News",
        "published": 1776401681,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L4N4100B5:0-apple-marketing-chief-for-watch-airpods-home-and-health-stan-ng-retires-bloomberg-news/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260416008149:0",
        "title": "TSMC's Results Weren't a Great Sign for Apple — Heard on the Street — WSJ",
        "published": 1776366900,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "TWSE:2330",
            "logoid": "taiwan-semiconductor"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "isExclusive": true,
        "storyPath": "/news/DJN_DN20260416008149:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260415008637:0",
        "title": "Former Apple Exec Leaves Ford in Tech Reorganization — Barrons.com",
        "published": 1776290160,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:F",
            "logoid": "ford"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          }
        ],
        "storyPath": "/news/DJN_DN20260415008637:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260415008356:0",
        "title": "The S&P 500 Just Surged to a Record High Despite a War. Why It May Keep Rising. — Barrons.com",
        "published": 1776286620,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "CBOE:SPX",
            "logoid": "indices/s-and-p-500"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          }
        ],
        "storyPath": "/news/DJN_DN20260415008356:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stockstory:7cf1a340f094b:0",
        "title": "Apple (AAPL) Stock Trades Up, Here Is Why",
        "published": 1776281751,
        "urgency": 2,
        "link": "https://stockstory.org/us/stocks/nasdaq/aapl/news/why-up-down/apple-aapl-stock-trades-up-here-is-why-4",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stockstory:7cf1a340f094b:0-apple-aapl-stock-trades-up-here-is-why/",
        "provider": {
          "id": "stockstory",
          "name": "Stock Story",
          "logo_id": "stockstory",
          "url": "https://stockstory.org/"
        }
      },
      {
        "id": "DJN_DN20260414007032:0",
        "title": "Apple and Amazon Partner on Satellite Deal. Why It Makes Sense. — Barrons.com",
        "published": 1776193740,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260414007032:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260414002395:0",
        "title": "Apple Is Maintained at Buy by B of A Securities",
        "published": 1776163380,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260414002395:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260410001611:0",
        "title": "Tech Trader: Apple Fell Behind With Gen-Z. The Neo Changed Everything. — Barron's",
        "published": 1775871000,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260410001611:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "dpa_afx:79a707a53529f:0",
        "title": "Apple To Shut Down 3 Retail Stores, Including First Unionized Outlet In Towson",
        "published": 1775844789,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/dpa_afx:79a707a53529f:0-apple-to-shut-down-3-retail-stores-including-first-unionized-outlet-in-towson/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "DJN_DN20260410003674:0",
        "title": "Anthropic Has Banks, Regulators Rattled Over AI Cyber Risks. Some Big Names Could Benefit. — Barrons.com",
        "published": 1775822820,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:CRWD",
            "logoid": "crowdstrike"
          },
          {
            "symbol": "NYSE:JPM",
            "logoid": "jpmorgan-chase"
          },
          {
            "symbol": "NASDAQ:PANW",
            "logoid": "palo-alto-networks"
          }
        ],
        "storyPath": "/news/DJN_DN20260410003674:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:eaf71f338094b:0",
        "title": "Apple Outperforms In Tough Q1 Even As Memory Crunch Drags Global Smartphone Shipments",
        "published": 1775820020,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-outperforms-in-tough-q1-even-as-memory-crunch-drags-global-smartphone-shipments/cZJ0a2PRIte",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:eaf71f338094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN40S1DJ:0",
        "title": "Later This Month, Apple TV To Be Available Via Prime Video In The U.S. As An Add-On Subscription For $9.99 Per Month",
        "published": 1775817039,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN40S1DJ:0-later-this-month-apple-tv-to-be-available-via-prime-video-in-the-u-s-as-an-add-on-subscription-for-9-99-per-month/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L4N40T0PA:0",
        "title": "Apple leads smartphone market even as overall shipments decline, Counterpoint says",
        "published": 1775815508,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "KRX:005930",
            "logoid": "samsung"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L4N40T0PA:0-apple-leads-smartphone-market-even-as-overall-shipments-decline-counterpoint-says/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L1N40T08B:0",
        "title": "Apple leads global smartphone shipments in first quarter, Counterpoint says",
        "published": 1775811689,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L1N40T08B:0-apple-leads-global-smartphone-shipments-in-first-quarter-counterpoint-says/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260409006711:0",
        "title": "Amazon Stock Jumps on DOJ's NFL Probe. It's About 'Affordability for Consumers.' — Barrons.com",
        "published": 1775766360,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NFLX",
            "logoid": "netflix"
          },
          {
            "symbol": "NASDAQ:PSKY",
            "logoid": "viacomcbs"
          }
        ],
        "storyPath": "/news/DJN_DN20260409006711:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_SN20260409009895:0",
        "title": "Big Tech stocks look like especially good deals as investors eye what is next for the market",
        "published": 1775748840,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:PLTR",
            "logoid": "palantir"
          }
        ],
        "storyPath": "/news/DJN_SN20260409009895:0/",
        "provider": {
          "id": "market-watch",
          "name": "MarketWatch",
          "logo_id": "marketwatch"
        }
      },
      {
        "id": "DJN_DN20260408006647:0",
        "title": "How Wall Street Went from Iran War Angst to Watching for a New S&P 500 Record — Barrons.com",
        "published": 1775667540,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "CBOE:SPX",
            "logoid": "indices/s-and-p-500"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NYSE:JPM",
            "logoid": "jpmorgan-chase"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          }
        ],
        "storyPath": "/news/DJN_DN20260408006647:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260408001215:0",
        "title": "Warren Buffett Is Retired. His Latest Advice Couldn't Be More Timely for Young Investors. — Barrons.com",
        "published": 1775629800,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:BRK.A",
            "logoid": "berkshire-hathaway"
          }
        ],
        "storyPath": "/news/DJN_DN20260408001215:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_SN20260407011240:0",
        "title": "Apple's stock pares losses. Here's how to think about the latest saga with foldable iPhones.",
        "published": 1775597460,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_SN20260407011240:0/",
        "provider": {
          "id": "market-watch",
          "name": "MarketWatch",
          "logo_id": "marketwatch"
        }
      },
      {
        "id": "DJN_DN20260407006693:0",
        "title": "Palo Alto, CrowdStrike Stocks Pop After Anthropic Announces Partnerships — Barrons.com",
        "published": 1775592540,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AVGO",
            "logoid": "broadcom"
          },
          {
            "symbol": "NASDAQ:CSCO",
            "logoid": "cisco"
          },
          {
            "symbol": "NASDAQ:CRWD",
            "logoid": "crowdstrike"
          },
          {
            "symbol": "NYSE:JPM",
            "logoid": "jpmorgan-chase"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:PANW",
            "logoid": "palo-alto-networks"
          }
        ],
        "storyPath": "/news/DJN_DN20260407006693:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN40Q02L:0",
        "title": "Apple’s Foldable iPhone Remains On Track For September Debut - Bloomberg News",
        "published": 1775581554,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN40Q02L:0-apple-s-foldable-iphone-remains-on-track-for-september-debut-bloomberg-news/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "stocktwits:3f6b9040a094b:0",
        "title": "AAPL Stock Slides As iPhone-Maker Faces Modest App Store Growth In Q1 – Retail Says ‘Great Opportunity’ To Buy More",
        "published": 1775580095,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/aapl-stock-slides-as-i-phone-maker-faces-modest-app-store-growth-in-q1-retail-says-great-opportunity-to-buy-more/cZJJUImRIpw",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:3f6b9040a094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_DN20260407005480:0",
        "title": "Apple Stock Drops on Foldable iPhone Delay Fears — Barrons.com",
        "published": 1775579460,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260407005480:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stockstory:df3b03abe094b:0",
        "title": "Why Apple (AAPL) Shares Are Falling Today",
        "published": 1775579443,
        "urgency": 2,
        "link": "https://stockstory.org/us/stocks/nasdaq/aapl/news/why-up-down/why-apple-aapl-shares-are-falling-today-3",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stockstory:df3b03abe094b:0-why-apple-aapl-shares-are-falling-today/",
        "provider": {
          "id": "stockstory",
          "name": "Stock Story",
          "logo_id": "stockstory",
          "url": "https://stockstory.org/"
        }
      },
      {
        "id": "DJN_DN20260407004720:0",
        "title": "Apple Shares Fall on Report of Foldable iPhone Engineering Setbacks",
        "published": 1775574720,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260407004720:0-apple-shares-fall-on-report-of-foldable-iphone-engineering-setbacks/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260407004477:0",
        "title": "Apple Stock Drags Down the Dow — WSJ",
        "published": 1775572500,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "TVC:DJI",
            "logoid": "indices/dow-30"
          }
        ],
        "storyPath": "/news/DJN_DN20260407004477:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260407000359:0",
        "title": "Big Tech and Banks Expected to Lead Solid Earnings Season. There Will Be Buying Opportunities. — Barrons.com",
        "published": 1775541600,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AVGO",
            "logoid": "broadcom"
          },
          {
            "symbol": "NYSE:JPM",
            "logoid": "jpmorgan-chase"
          },
          {
            "symbol": "NYSE:MS",
            "logoid": "morgan-stanley"
          }
        ],
        "storyPath": "/news/DJN_DN20260407000359:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L4N40Q06P:0",
        "title": "Apple's foldable iPhone faces engineering snags, potential shipment delays, Nikkei Asia reports",
        "published": 1775532148,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L4N40Q06P:0-apple-s-foldable-iphone-faces-engineering-snags-potential-shipment-delays-nikkei-asia-reports/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L4N40Q061:0",
        "title": "Apple's foldable iPhone encounters engineering snags, faces potential shipment delays, Nikkei Asia reports",
        "published": 1775530403,
        "urgency": 1,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L4N40Q061:0-apple-s-foldable-iphone-encounters-engineering-snags-faces-potential-shipment-delays-nikkei-asia-reports/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260406003372:0",
        "title": "AI Is Squeezing Memory Supplies. How Apple's Strategy Can Boost Its Stock. — Barrons.com",
        "published": 1775492760,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:DELL",
            "logoid": "dell"
          },
          {
            "symbol": "NYSE:HPQ",
            "logoid": "hp"
          }
        ],
        "storyPath": "/news/DJN_DN20260406003372:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_SN20260406003478:0",
        "title": "Apple's stock could surge 20%, and the MacBook Neo could be a key catalyst",
        "published": 1775492640,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_SN20260406003478:0/",
        "provider": {
          "id": "market-watch",
          "name": "MarketWatch",
          "logo_id": "marketwatch"
        }
      },
      {
        "id": "DJN_DN20260403001003:0",
        "title": "SpaceX Is Worth $2 Trillion? What That Might Mean. — Barrons.com",
        "published": 1775244360,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          }
        ],
        "storyPath": "/news/DJN_DN20260403001003:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260403002001:0",
        "title": "I Looked Inside the First iPhone and Saw 50 Years of Apple History — WSJ",
        "published": 1775231100,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260403002001:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_SN20260402006665:0",
        "title": "Venture capitalist who bet on Apple nearly 50 years ago: Questionable management, price is rich, but 'home-hobby computers' are hot",
        "published": 1775140260,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_SN20260402006665:0/",
        "provider": {
          "id": "market-watch",
          "name": "MarketWatch",
          "logo_id": "marketwatch"
        }
      },
      {
        "id": "dpa_afx:4ad72a40de37f:0",
        "title": "Apple @ 50: Five Decades Of Reinvention",
        "published": 1775052285,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/dpa_afx:4ad72a40de37f:0-apple-50-five-decades-of-reinvention/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "DJN_DN20260401002674:0",
        "title": "Buffett Isn't Getting Carried Away by This Iran Trump Bump. Neither Should Markets. — Barrons.com",
        "published": 1775039580,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:CEG",
            "logoid": "constellation-energy-cad-hedged-cibc-cdr"
          },
          {
            "symbol": "NYSE:DIS",
            "logoid": "walt-disney"
          },
          {
            "symbol": "NYSE:LMT",
            "logoid": "lockheed-martin"
          },
          {
            "symbol": "NYSE:NOC",
            "logoid": "northrop-grumman"
          }
        ],
        "storyPath": "/news/DJN_DN20260401002674:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L4N40K0QN:0",
        "title": "Apple's 50-year journey from garage to tech titan",
        "published": 1775037600,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L4N40K0QN:0-apple-s-50-year-journey-from-garage-to-tech-titan/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260331006152:0",
        "title": "Apple Turns 50. The iPhone Can't Drive the Stock Forever. — Barrons.com",
        "published": 1774988580,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260331006152:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260331008339:0",
        "title": "Apple Expected to Detail AI Advancements at 2026 WWDC — Market Talk",
        "published": 1774977600,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260331008339:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L4N40J1QM:0",
        "title": "Apple tests Siri feature that handles multiple commands at once, Bloomberg News reports",
        "published": 1774974295,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L4N40J1QM:0-apple-tests-siri-feature-that-handles-multiple-commands-at-once-bloomberg-news-reports/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260331004886:0",
        "title": "Warren Buffett Sees Little to Buy in the Stock Market After This Year's Drop — Barrons.com",
        "published": 1774971360,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NYSE:BRK.A",
            "logoid": "berkshire-hathaway"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "TVC:DJI",
            "logoid": "indices/dow-30"
          }
        ],
        "storyPath": "/news/DJN_DN20260331004886:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260331006959:0",
        "title": "Apple Price Target Maintained With a $350.00/Share by Wedbush",
        "published": 1774968840,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260331006959:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L6N40J177:0",
        "title": "Warren Buffett discusses markets, Apple, Jeffrey Epstein, Gates Foundation on CNBC",
        "published": 1774962093,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NYSE:BRK.A",
            "logoid": "berkshire-hathaway"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L6N40J177:0-warren-buffett-discusses-markets-apple-jeffrey-epstein-gates-foundation-on-cnbc/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260329000049:0",
        "title": "Correction to Everyone Hates iPhone Autocorrect Article on March 29 — WSJ",
        "published": 1774897860,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260329000049:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "dpa_afx:46d65658f83f8:0",
        "title": "UK Fines Apple Subsidiary £390,000 Over Russia Sanctions Breach",
        "published": 1774882533,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/dpa_afx:46d65658f83f8:0-uk-fines-apple-subsidiary-390-000-over-russia-sanctions-breach/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L8N40F0VG:0",
        "title": "What is the World Trade Organization e-commerce moratorium?",
        "published": 1774704337,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L8N40F0VG:0-what-is-the-world-trade-organization-e-commerce-moratorium/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L6N40F11D:0",
        "title": "Apple hires ex-Google executive to head AI marketing amid push to improve Siri",
        "published": 1774632658,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L6N40F11D:0-apple-hires-ex-google-executive-to-head-ai-marketing-amid-push-to-improve-siri/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260327005265:0",
        "title": "All Eyes Back on Apple's AI Strategy As 50th Anniversary — Market Talk",
        "published": 1774617540,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260327005265:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260326010953:0",
        "title": "Netflix's Prices Are Going Up. Don't Expect Streaming to Get Cheaper Soon. — Barrons.com",
        "published": 1774614540,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:DIS",
            "logoid": "walt-disney"
          },
          {
            "symbol": "NASDAQ:NFLX",
            "logoid": "netflix"
          },
          {
            "symbol": "NASDAQ:PSKY",
            "logoid": "viacomcbs"
          }
        ],
        "storyPath": "/news/DJN_DN20260326010953:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "dpa_afx:8a7391661267a:0",
        "title": "Apple Adds New Partners, To Invest $400 Mln To Expand US Manufacturing",
        "published": 1774611960,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "TSE:6762",
            "logoid": "tdk"
          },
          {
            "symbol": "NASDAQ:CRUS",
            "logoid": "cirrus-logic"
          }
        ],
        "storyPath": "/news/dpa_afx:8a7391661267a:0-apple-adds-new-partners-to-invest-400-mln-to-expand-us-manufacturing/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN40E16L:0",
        "title": "Apple Has Discontinued Mac Pro And Has Removed It From Its Website - Bloomberg News Reporter Gurman",
        "published": 1774559227,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN40E16L:0-apple-has-discontinued-mac-pro-and-has-removed-it-from-its-website-bloomberg-news-reporter-gurman/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN40E16J:0",
        "title": "Apple Gives iPhone Designers Rare Bonuses To Fight OpenAI Poaching - Bloomberg News",
        "published": 1774557668,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN40E16J:0-apple-gives-iphone-designers-rare-bonuses-to-fight-openai-poaching-bloomberg-news/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260326009594:0",
        "title": "Apple Stock Has Been Weak This Year. Why Analysts Think Better Times Are Ahead. — Barrons.com",
        "published": 1774557000,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260326009594:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN40E14R:0",
        "title": "Apple Plans To Open Up Siri To Rival AI Assistants In iOS 27 Update - Bloomberg News",
        "published": 1774548846,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN40E14R:0-apple-plans-to-open-up-siri-to-rival-ai-assistants-in-ios-27-update-bloomberg-news/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L4N40E0ZU:0",
        "title": "Apple adds Bosch, Cirrus Logic, others to US manufacturing program, to invest $400 million",
        "published": 1774530538,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:CRUS",
            "logoid": "cirrus-logic"
          },
          {
            "symbol": "TSE:6762",
            "logoid": "tdk"
          },
          {
            "symbol": "NYSE:Q",
            "logoid": "qnity-electronics"
          },
          {
            "symbol": "TWSE:2330",
            "logoid": "taiwan-semiconductor"
          },
          {
            "symbol": "NASDAQ:GFS",
            "logoid": "globalfoundries"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L4N40E0ZU:0-apple-adds-bosch-cirrus-logic-others-to-us-manufacturing-program-to-invest-400-million/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260325006992:0",
        "title": "Microsoft Stock Tracking Worst 6-Month Stretch Since 2009 — Barrons.com",
        "published": 1774471980,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AVGO",
            "logoid": "broadcom"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NYSE:SNOW",
            "logoid": "snowflake"
          }
        ],
        "storyPath": "/news/DJN_DN20260325006992:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260325007265:0",
        "title": "Amplification for Apple Cuts App Store Fees in China Article on March 13 — WSJ",
        "published": 1774464720,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260325007265:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "dpa_afx:b59c1ac2b1b02:0",
        "title": "Apple Introduces Age Verification For UK Users",
        "published": 1774455929,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/dpa_afx:b59c1ac2b1b02:0-apple-introduces-age-verification-for-uk-users/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_P8N3ZR082:0",
        "title": "February shipments of foreign-branded phones in China fall 7.7% from a year ago, CAICT data shows",
        "published": 1774420658,
        "urgency": 1,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_P8N3ZR082:0-february-shipments-of-foreign-branded-phones-in-china-fall-7-7-from-a-year-ago-caict-data-shows/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260324008889:0",
        "title": "HP Inc. Announces AI Updates. Your Turn, Apple. — Barrons.com",
        "published": 1774388400,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:HPQ",
            "logoid": "hp"
          }
        ],
        "storyPath": "/news/DJN_DN20260324008889:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN40C10O:0",
        "title": "Apple Plans AI Reboot With Siri App, New Look And ‘Ask Siri’ Button In IOS 27 - Bloomberg News",
        "published": 1774378664,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN40C10O:0-apple-plans-ai-reboot-with-siri-app-new-look-and-ask-siri-button-in-ios-27-bloomberg-news/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L1N40C0TO:0",
        "title": "Apple to bring paid ads to maps to US, Canada this summer",
        "published": 1774367569,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L1N40C0TO:0-apple-to-bring-paid-ads-to-maps-to-us-canada-this-summer/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L6N40C0UP:0",
        "title": "Apple to bring paid ads to maps to US, Canada this summer ",
        "published": 1774364400,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L6N40C0UP:0-apple-to-bring-paid-ads-to-maps-to-us-canada-this-summer/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260323006307:0",
        "title": "Apple iPhone Demand Is Getting Multiple Boosts, Analysts Say. The Stock Rises. — Barrons.com",
        "published": 1774289700,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260323006307:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260323006259:0",
        "title": "Apple Price Target Maintained With a $315.00/Share by Morgan Stanley",
        "published": 1774289100,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260323006259:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L4N40B1LQ:0",
        "title": "Apple to hold annual developers conference from June 8",
        "published": 1774287883,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L4N40B1LQ:0-apple-to-hold-annual-developers-conference-from-june-8/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L4N40B1L0:0",
        "title": "Apple to hold annual developers conference in June",
        "published": 1774285485,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L4N40B1L0:0-apple-to-hold-annual-developers-conference-in-june/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN40B0TN:0",
        "title": "Apple Is Set To Add Search Advertising To Maps In Services Push, An Announcement Could Come As Early As This Month- Bloomberg News",
        "published": 1774284697,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN40B0TN:0-apple-is-set-to-add-search-advertising-to-maps-in-services-push-an-announcement-could-come-as-early-as-this-month-bloomberg-news/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L6N40815C:0",
        "title": "Amazon plans smartphone comeback more than a decade after Fire Phone flop",
        "published": 1774041610,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "isExclusive": true,
        "storyPath": "/news/reuters.com,2026:newsml_L6N40815C:0-amazon-plans-smartphone-comeback-more-than-a-decade-after-fire-phone-flop/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260320006638:0",
        "title": "Apple's Latest Launch Was 'Best' Ever for New Mac Customers. What It Means for the Stock. — Barrons.com",
        "published": 1774038720,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:DELL",
            "logoid": "dell"
          },
          {
            "symbol": "NYSE:HPQ",
            "logoid": "hp"
          }
        ],
        "storyPath": "/news/DJN_DN20260320006638:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_P8N3YM04J:0",
        "title": "China's commerce minister meets Apple CEO",
        "published": 1773995981,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_P8N3YM04J:0-china-s-commerce-minister-meets-apple-ceo/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260319007716:0",
        "title": "Apple's China iPhone Sales Are Up. Thank Memory Cost Increases. — Barrons.com",
        "published": 1773942660,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260319007716:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L6N3WF0SO:0",
        "title": "Apple fends off bid for new Apple Watch import ban at US trade tribunal ",
        "published": 1773936720,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MASI",
            "logoid": "masimo"
          },
          {
            "symbol": "NYSE:DHR",
            "logoid": "danaher"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L6N3WF0SO:0-apple-fends-off-bid-for-new-apple-watch-import-ban-at-us-trade-tribunal/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L8N40701A:0",
        "title": "Apple's China smartphone sales jump 23% to start 2026, bucking industry trend",
        "published": 1773886610,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L8N40701A:0-apple-s-china-smartphone-sales-jump-23-to-start-2026-bucking-industry-trend/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260318009535:0",
        "title": "Apple Is Way Behind in AI — and Still Making a Fortune From It — WSJ",
        "published": 1773882000,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260318009535:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260318001539:0",
        "title": "Sure, Nvidia Stock Is Stuck. But Don't Ignore Its Huge Cash Returns. — Barrons.com",
        "published": 1773864480,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/DJN_DN20260318001539:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN4060M6:0",
        "title": "Apple Says Some AI Vibe Coding Apps Violate App Store Rules By Running Code That Alters App Functionality - The Information",
        "published": 1773839002,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN4060M6:0-apple-says-some-ai-vibe-coding-apps-violate-app-store-rules-by-running-code-that-alters-app-functionality-the-information/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260318000052:0",
        "title": "Apple's App Store Fee Cut in China Offers Tailwind for Tencent, NetEase — Market Talk",
        "published": 1773807120,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NTES",
            "logoid": "netease"
          },
          {
            "symbol": "HKEX:700",
            "logoid": "tencent"
          }
        ],
        "storyPath": "/news/DJN_DN20260318000052:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:adc733d48094b:0",
        "title": "Apple Loses Top Hardware Executive To Smart Ring Maker Oura Health Amid Product Delays: Report",
        "published": 1773786003,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-loses-top-hardware-executive-to-smart-ring-maker-oura-health-amid-product-delays-report/cZ3Ek3bRIXx",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:adc733d48094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN4050SG:0",
        "title": "Apple’S Head Of Home Hardware Brian Lynch Leaves For Smart Ring Maker Oura - Bloomberg News",
        "published": 1773785305,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN4050SG:0-apple-s-head-of-home-hardware-brian-lynch-leaves-for-smart-ring-maker-oura-bloomberg-news/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260317006382:0",
        "title": "Apple CEO Squashes Talk of Stepping Down — Market Talk",
        "published": 1773767340,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260317006382:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:ec5a08cb6094b:0",
        "title": "Apple’s Tim Cook Shuts Down Retirement Buzz, Says He ‘Deeply’ Loves His Job",
        "published": 1773765924,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-tim-cook-shuts-down-retirement-buzz-says-he-deeply-loves-his-job/cZ3Ea4yRIXk",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:ec5a08cb6094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "dpa_afx:5b58a8bad361e:0",
        "title": "Apple Launches AirPods Max 2 With Improved ANC And H2 Chip",
        "published": 1773685935,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/dpa_afx:5b58a8bad361e:0-apple-launches-airpods-max-2-with-improved-anc-and-h2-chip/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "DJN_DN20260316006424:0",
        "title": "Apple Acquires MotionVFX",
        "published": 1773680700,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260316006424:0-apple-acquires-motionvfx/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260316005558:0",
        "title": "Apple Announced AirPods Max 2, Starting at $549 — Market Talk",
        "published": 1773676260,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260316005558:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L6N4040XN:0",
        "title": "Apple unveils second-generation AirPods Max at $549, more than five years after debut",
        "published": 1773668798,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "TSE:6758",
            "logoid": "sony"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L6N4040XN:0-apple-unveils-second-generation-airpods-max-at-549-more-than-five-years-after-debut/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260314000775:0",
        "title": "Review: Does the $599 MacBook Neo Fit in Your Life? — WSJ",
        "published": 1773495120,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260314000775:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260313003272:0",
        "title": "Apple Reduces China App Store Fees as It Fends Off Pressure From Beijing — Barrons.com",
        "published": 1773409860,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260313003272:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260313004404:0",
        "title": "Meta Is Falling Behind in AI Models. Its Loss Could Be Google's Gain, Report Says. — Barrons.com",
        "published": 1773408240,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          }
        ],
        "storyPath": "/news/DJN_DN20260313004404:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:0fcb83f3b094b:0",
        "title": "Apple Bows To Chinese Regulatory Pressure With App Store Fee Cut: These Firms Could Be The Big Winners",
        "published": 1773391474,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-bows-to-chinese-regulatory-pressure-with-app-store-fee-cut/cZdDEsRRIaN",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:0fcb83f3b094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_DN20260313001151:0",
        "title": "Apple Cuts App Store Fees in China as Regulatory Scrutiny Intensifies — Update",
        "published": 1773384300,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260313001151:0-apple-cuts-app-store-fees-in-china-as-regulatory-scrutiny-intensifies-update/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260313000127:0",
        "title": "Apple's Commission Cut Bodes Well for Chinese Game Developers — Market Talk",
        "published": 1773378360,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:NTES",
            "logoid": "netease"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "HKEX:700",
            "logoid": "tencent"
          }
        ],
        "storyPath": "/news/DJN_DN20260313000127:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260312013664:0",
        "title": "Apple Cuts App Store Commission Fees in China",
        "published": 1773374160,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260312013664:0-apple-cuts-app-store-commission-fees-in-china/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:7499a5168094b:0",
        "title": "Is Himax A ‘Stealth’ Supplier To Nvidia, Apple? HIMX Stock Pops To Nearly 1-Year High After Hedge Fund Flags Possible Links",
        "published": 1773368534,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/is-himax-a-stealth-supplier-to-nvidia-apple-himx-stock-pops-to-nearly-1-year-high-after-hedge-fund-flags-possible-links/cZdwxZ1RIaB",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:HIMX",
            "logoid": "himax-technologies"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/stocktwits:7499a5168094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_DN20260312013523:0",
        "title": "Global Smartphone Shipments Could Fall 17% in 2026 — Market Talk",
        "published": 1773368280,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "KRX:005930",
            "logoid": "samsung"
          },
          {
            "symbol": "HKEX:1810",
            "logoid": "xiaomi"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260312013523:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260312012252:0",
        "title": "Monster, Palantir, and Other Stocks That Can Weather the Market Storm — Barrons.com",
        "published": 1773352140,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MNST",
            "logoid": "monster-beverage"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:PLTR",
            "logoid": "palantir"
          }
        ],
        "storyPath": "/news/DJN_DN20260312012252:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260312007814:0",
        "title": "FTC Release: Federal Trade Commission Chairman Andrew N. Ferguson Issues Warning Letter to Apple CEO Tim Cook",
        "published": 1773329820,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260312007814:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L1N4000GL:0",
        "title": "India plans fresh incentives for phone production in boost for Apple, Samsung",
        "published": 1773315519,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "KRX:005930",
            "logoid": "samsung"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L1N4000GL:0-india-plans-fresh-incentives-for-phone-production-in-boost-for-apple-samsung/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN3ZZ16X:0",
        "title": "Apple's Forthcoming Foldable iPhone Will Feature An Interior Foldable Display Roughly The Size Of An iPad Mini - Bloomberg News",
        "published": 1773260038,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN3ZZ16X:0-apple-s-forthcoming-foldable-iphone-will-feature-an-interior-foldable-display-roughly-the-size-of-an-ipad-mini-bloomberg-news/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "stocktwits:6fb9f49d5094b:0",
        "title": "Laptop Prices Could Rise Up To 40% In 2026: How Apple, HP And Dell Are Plotting To Navigate Rising Memory Prices",
        "published": 1773220767,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/laptop-prices-could-rise-up-to-40-in-2026-how-apple-hp-and-dell-are-plotting-to-navigate-rising-memory-prices/cZdAMLuRIJf",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NYSE:DELL",
            "logoid": "dell"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:HPQ",
            "logoid": "hp"
          }
        ],
        "storyPath": "/news/stocktwits:6fb9f49d5094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_DN20260310008536:0",
        "title": "Apple's Budget MacBook Is a Hit. What It Means For the Stock, and What's Next. — Barrons.com",
        "published": 1773167940,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260310008536:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260310005451:0",
        "title": "German Ad Groups Say Changes to Apple's App-Tracking Tool Aren't Enough",
        "published": 1773146400,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260310005451:0-german-ad-groups-say-changes-to-apple-s-app-tracking-tool-aren-t-enough/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:fca095bd1094b:0",
        "title": "Apple Delays Smart Home Device Once More Amid New AI, Siri Setback: Report",
        "published": 1773082815,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-delays-smart-home-device-once-more-amid-new-ai-siri-setback-report/cZdVuFuRIeR",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:fca095bd1094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN3ZX125:0",
        "title": "Apple Postpones Smart Home Display Launch As It Waits For New AI, Siri - Bloomberg News",
        "published": 1773082443,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN3ZX125:0-apple-postpones-smart-home-display-launch-as-it-waits-for-new-ai-siri-bloomberg-news/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260309003955:0",
        "title": "Apple Faces a Memory Crunch. Why Analysts Say the Stock Is Still a Buy. — Barrons.com",
        "published": 1773057780,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260309003955:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260305001184:0",
        "title": "Up & Down Wall Street: How the Mag 7 Became the Lag 7 — Barron's",
        "published": 1772850600,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          }
        ],
        "storyPath": "/news/DJN_DN20260305001184:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260306006471:0",
        "title": "3 Dividend ETFs for Shelter in These Stormy Times — Barrons.com",
        "published": 1772820900,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AVGO",
            "logoid": "broadcom"
          },
          {
            "symbol": "NYSE:KO",
            "logoid": "coca-cola"
          },
          {
            "symbol": "NYSE:COP",
            "logoid": "conocophillips"
          },
          {
            "symbol": "NYSE:LMT",
            "logoid": "lockheed-martin"
          }
        ],
        "storyPath": "/news/DJN_DN20260306006471:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:bad99ff54094b:0",
        "title": "‘Big Short’ Fame Michael Burry Pitches Bold AI Deal Ideas For Apple, Adobe — And Fires Shots At Tesla CEO Elon Musk",
        "published": 1772772649,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/big-short-fame-michael-burry-pitches-bold-ai-deal-ideas-for-apple-adobe-and-fires-shots-at-tesla-ceo-elon-musk/cZdhnSmRIEJ",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:ANTHROPIC",
            "logoid": "anthropic"
          }
        ],
        "storyPath": "/news/stocktwits:bad99ff54094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_DN20260305009360:0",
        "title": "This ETF Was Built for This Very Moment. So Why Hasn't It Done Well? — Barrons.com",
        "published": 1772746980,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/DJN_DN20260305009360:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260305009544:0",
        "title": "Cheaper iPhones and a $599 MacBook? Apple Is All About Affordability Now. — Barrons.com",
        "published": 1772746680,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:DELL",
            "logoid": "dell"
          },
          {
            "symbol": "NYSE:HPQ",
            "logoid": "hp"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/DJN_DN20260305009544:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "dpa_afx:7cb6395cea3f4:0",
        "title": "Apple Music To Add Transparency Tags For AI-Generated Music",
        "published": 1772744961,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/dpa_afx:7cb6395cea3f4:0-apple-music-to-add-transparency-tags-for-ai-generated-music/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "DJN_DN20260305006608:0",
        "title": "Apple Is Maintained at Neutral by Rosenblatt",
        "published": 1772718960,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260305006608:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260304012892:0",
        "title": "MacBook Neo and iPhone 17e First Impressions: The Return of Cheap and Cheerful — Personal Technology — WSJ",
        "published": 1772676000,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260304012892:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "dpa_afx:2859ab73a8cb7:0",
        "title": "Apple Launches MacBook Neo Starting At $599",
        "published": 1772649459,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/dpa_afx:2859ab73a8cb7:0-apple-launches-macbook-neo-starting-at-599/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "DJN_DN20260304007584:0",
        "title": "Apple's Price Increases Soothe Concerns Over Memory Costs — Market Talk",
        "published": 1772645640,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260304007584:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260304006806:0",
        "title": "Apple Launches a $599 MacBook. Why That Price Is Such a Big Deal. — Barrons.com",
        "published": 1772644500,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:DELL",
            "logoid": "dell"
          },
          {
            "symbol": "NYSE:HPQ",
            "logoid": "hp"
          }
        ],
        "storyPath": "/news/DJN_DN20260304006806:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260304007387:0",
        "title": "Apple Uses Low Prices to Attack Rivals During Memory-Chip Crunch — WSJ",
        "published": 1772644260,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260304007387:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260304007302:0",
        "title": "Apple Seen Getting a Lift from New Mac Laptops — Market Talk",
        "published": 1772644080,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260304007302:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:930831ece094b:0",
        "title": "Apple Launches MacBook Neo At $599, Offering An Alternative To Google’s Chromebooks",
        "published": 1772639380,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-launches-macbook-neo-starting-at-599-taking-on-google-chromebooks/cZd9YtyRI5z",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:930831ece094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_DN20260304006275:0",
        "title": "Apple's $599 MacBook Neo: The Pros and Cons — WSJ",
        "published": 1772637960,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260304006275:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L6N3ZS157:0",
        "title": "Apple debuts $599 MacBook Neo to challenge Chromebooks, Windows PCs",
        "published": 1772634439,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:ARM",
            "logoid": "arm"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L6N3ZS157:0-apple-debuts-599-macbook-neo-to-challenge-chromebooks-windows-pcs/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "stocktwits:ec0a965c0094b:0",
        "title": "AAPL, MSFT, CRWD, PANW: Dan Ives Identifies Top Tech Names Positioned To Navigate US-Iran War-Led Volatility",
        "published": 1772632599,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/aapl-msft-crwd-panw-dan-ives-identifies-top-tech-names-positioned-to-navigate-us-iran-war-led-volatility/cZd9VsnRI5t",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:CRWD",
            "logoid": "crowdstrike"
          },
          {
            "symbol": "NASDAQ:PANW",
            "logoid": "palo-alto-networks"
          }
        ],
        "storyPath": "/news/stocktwits:ec0a965c0094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_P8N3YS0DA:0",
        "title": "Shipments of foreign-branded phones in China fell in Jan on-year, CAICT data says",
        "published": 1772589432,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_P8N3YS0DA:0-shipments-of-foreign-branded-phones-in-china-fell-in-jan-on-year-caict-data-says/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "dpa_afx:17468bd159475:0",
        "title": "Apple Explores Deepening Google Partnership For Next-Gen Siri",
        "published": 1772576758,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/dpa_afx:17468bd159475:0-apple-explores-deepening-google-partnership-for-next-gen-siri/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "dpa_afx:916e3ad594757:0",
        "title": "Apple Unveils New Studio Display Lineup, Introduces Studio Display XDR",
        "published": 1772574784,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/dpa_afx:916e3ad594757:0-apple-unveils-new-studio-display-lineup-introduces-studio-display-xdr/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "DJN_DN20260303008032:0",
        "title": "This Schwab Dividend ETF is a Superstar. Defense and Energy Are Key — Barrons.com",
        "published": 1772566800,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AVGO",
            "logoid": "broadcom"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:MORN",
            "logoid": "morningstar"
          }
        ],
        "storyPath": "/news/DJN_DN20260303008032:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "dpa_afx:fb10a1085b6ba:0",
        "title": "Apple Launches M5 Pro And M5 Max With Major Performance Boost",
        "published": 1772563012,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/dpa_afx:fb10a1085b6ba:0-apple-launches-m5-pro-and-m5-max-with-major-performance-boost/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "dpa_afx:2c972b4358f9c:0",
        "title": "Apple Unveils MacBook Air With M5 Chip",
        "published": 1772560785,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/dpa_afx:2c972b4358f9c:0-apple-unveils-macbook-air-with-m5-chip/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "DJN_DN20260303001337:0",
        "title": "Should You Buy the Stock Market's Dip? Why the Mideast Fighting Could Be an Opportunity. — Barrons.com",
        "published": 1772556300,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/DJN_DN20260303001337:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260303006394:0",
        "title": "Apple Launches New Laptops and Chips. AI Power Is a Focus. — Barrons.com",
        "published": 1772554920,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260303006394:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260303006023:0",
        "title": "Apple Is Maintained at Underweight by Barclays",
        "published": 1772551920,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260303006023:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:bfad4995e094b:0",
        "title": "Apple Increases Prices Of Its New MacBook Air And Pro Models – Everything To Know About Its Latest Lineup",
        "published": 1772549519,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-increases-prices-of-its-new-mac-book-air-and-pro-models-everything-to-know-about-its-latest-lineup/cZdeK53RIPf",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:bfad4995e094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "dpa_afx:7f5b6e0b4c913:0",
        "title": "Apple Introduces M4-Powered IPad Air With 12GB Memory, Starting At $599",
        "published": 1772488648,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/dpa_afx:7f5b6e0b4c913:0-apple-introduces-m4-powered-ipad-air-with-12gb-memory-starting-at-599/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "stocktwits:d413ae839094b:0",
        "title": "Apple’s New iPhone 17e To Boost Sales From Price-Focused Buyers, Says Gene Munster",
        "published": 1772476910,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-iphone-17e-to-boost-sales-from-price-focused-buyers-says-gene-munster/cZd3i5GRI2W",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:d413ae839094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_DN20260302008113:0",
        "title": "Apple Faces Risk of Slower Demand for Next iPhone — Market Talk",
        "published": 1772476560,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260302008113:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "dpa_afx:843ffe90d6293:0",
        "title": "Apple Unveils IPhone 17e With A19 Chip, Improved Camera And Satellite Features",
        "published": 1772475902,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/dpa_afx:843ffe90d6293:0-apple-unveils-iphone-17e-with-a19-chip-improved-camera-and-satellite-features/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "DJN_DN20260302006227:0",
        "title": "Apple's 'Affordable' New iPhone 17e: Why You Should — or Shouldn't — Get It — WSJ",
        "published": 1772463720,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260302006227:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:7c6065ec9094b:0",
        "title": "Apple Launches iPhone 17e With A19 Chip, Advanced Camera",
        "published": 1772461866,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-launches-i-phone-17e-with-a19-chip-advanced-camera/cZd3BiGRI25",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:7c6065ec9094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN3ZQ0WW:0",
        "title": "Apple Discusses Google Hosting New Siri, Deepening Cloud Reliance- The Information",
        "published": 1772460305,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN3ZQ0WW:0-apple-discusses-google-hosting-new-siri-deepening-cloud-reliance-the-information/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260228000971:0",
        "title": "Berkshire Hathaway's CEO Suggests These 4 Companies Are Forever Stocks — Barrons.com",
        "published": 1772314920,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NYSE:AXP",
            "logoid": "american-express"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:BRK.A",
            "logoid": "berkshire-hathaway"
          },
          {
            "symbol": "NYSE:KO",
            "logoid": "coca-cola"
          },
          {
            "symbol": "NYSE:MCO",
            "logoid": "moodys"
          }
        ],
        "storyPath": "/news/DJN_DN20260228000971:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L6N3ZO0AO:0",
        "title": "Berkshire CEO Abel assures investors he'll be a careful steward after Buffett",
        "published": 1772286285,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NYSE:BRK.A",
            "logoid": "berkshire-hathaway"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:AXP",
            "logoid": "american-express"
          },
          {
            "symbol": "NYSE:KO",
            "logoid": "coca-cola"
          },
          {
            "symbol": "NYSE:MCO",
            "logoid": "moodys"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L6N3ZO0AO:0-berkshire-ceo-abel-assures-investors-he-ll-be-a-careful-steward-after-buffett/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN3ZO0B9:0",
        "title": "Berkshire Hathaway Reported $373.3 Billion Of Cash And Equivalents As Of December 31, 2025",
        "published": 1772286043,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:AXP",
            "logoid": "american-express"
          },
          {
            "symbol": "NYSE:BAC",
            "logoid": "bank-of-america"
          },
          {
            "symbol": "NYSE:BRK.A",
            "logoid": "berkshire-hathaway"
          },
          {
            "symbol": "NYSE:CVX",
            "logoid": "chevron"
          },
          {
            "symbol": "NYSE:KO",
            "logoid": "coca-cola"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN3ZO0B9:0-berkshire-hathaway-reported-373-3-billion-of-cash-and-equivalents-as-of-december-31-2025/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L6N3ZO0AF:0",
        "title": "Berkshire Hathaway profit falls on writedowns, lower insurance income",
        "published": 1772285132,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NYSE:BRK.A",
            "logoid": "berkshire-hathaway"
          },
          {
            "symbol": "NASDAQ:KHC",
            "logoid": "kraft-heinz"
          },
          {
            "symbol": "NYSE:OXY",
            "logoid": "occidental-petroleum"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:AXP",
            "logoid": "american-express"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L6N3ZO0AF:0-berkshire-hathaway-profit-falls-on-writedowns-lower-insurance-income/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "dpa_afx:a1be740354182:0",
        "title": "Apple's Latest IPhones And IPads Approved For NATO-Restricted Information",
        "published": 1772226888,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/dpa_afx:a1be740354182:0-apple-s-latest-iphones-and-ipads-approved-for-nato-restricted-information/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "DJN_DN20260227008205:0",
        "title": "How to Fight AI? The 'Rolex Effect' Could Lift Apple and Other Consumer Brands — Barrons.com",
        "published": 1772213100,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:MCD",
            "logoid": "mcdonalds"
          },
          {
            "symbol": "NASDAQ:WMT",
            "logoid": "walmart"
          }
        ],
        "storyPath": "/news/DJN_DN20260227008205:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260227005259:0",
        "title": "Stocks Are Set for a February Slide. Can the Magnificent 7 Spark a March Rebound? — Barrons.com",
        "published": 1772196000,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          }
        ],
        "storyPath": "/news/DJN_DN20260227005259:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:a55a75590094b:0",
        "title": "Apple’s AI Woes Meet A ‘Tsunami-Like’ Shock: IDC Sees Smartphone Shipments Crashing This Year",
        "published": 1772178224,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-s-ai-woes-meet-a-tsunami-like-shock-idc-sees-smartphone-shipments-crashing-this-year/cZTc9VjRIRH",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:a55a75590094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L4N3ZM253:0",
        "title": "Smartphone market set for biggest-ever decline in 2026 on memory price surge, IDC says",
        "published": 1772133573,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "KRX:005930",
            "logoid": "samsung"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L4N3ZM253:0-smartphone-market-set-for-biggest-ever-decline-in-2026-on-memory-price-surge-idc-says/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_SN20260226013776:0",
        "title": "These S&P 500 alternatives have shined so far this year",
        "published": 1772122560,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "CBOE:SPX",
            "logoid": "indices/s-and-p-500"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "AMEX:RSP",
            "logoid": "invesco"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/DJN_SN20260226013776:0/",
        "provider": {
          "id": "market-watch",
          "name": "MarketWatch",
          "logo_id": "marketwatch"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L6N3ZM0WB:0",
        "title": "Apple seeks dismissal of fraud lawsuit over Siri AI, Epic injunction",
        "published": 1772121551,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L6N3ZM0WB:0-apple-seeks-dismissal-of-fraud-lawsuit-over-siri-ai-epic-injunction/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L4N3ZM0I5:0",
        "title": "Apple in talks with banks to start payment service in India, Bloomberg News reports",
        "published": 1772087567,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NSE:ICICIBANK",
            "logoid": "icici-bank"
          },
          {
            "symbol": "NSE:HDFCBANK",
            "logoid": "hdfc-bank"
          },
          {
            "symbol": "NSE:AXISBANK",
            "logoid": "axis-bank"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L4N3ZM0I5:0-apple-in-talks-with-banks-to-start-payment-service-in-india-bloomberg-news-reports/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN3ZL29P:0",
        "title": "Apple In Talks With Banks To Start Payment Service In India - Bloomberg News",
        "published": 1772087389,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN3ZL29P:0-apple-in-talks-with-banks-to-start-payment-service-in-india-bloomberg-news/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260225008335:0",
        "title": "What I Saw Inside Apple's U.S. Chip Supply Chain — WSJ",
        "published": 1772049240,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "TWSE:2330",
            "logoid": "taiwan-semiconductor"
          }
        ],
        "storyPath": "/news/DJN_DN20260225008335:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260225009010:0",
        "title": "Apple Needs to Copy Samsung's New Security Smartphone Screen ASAP — WSJ",
        "published": 1772043120,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "KRX:005930",
            "logoid": "samsung"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260225009010:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L1N3ZL0OL:0",
        "title": "Apple and Amazon took too long to remove anti-competitive clauses, Spanish watchdog says",
        "published": 1772030407,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L1N3ZL0OL:0-apple-and-amazon-took-too-long-to-remove-anti-competitive-clauses-spanish-watchdog-says/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260225006487:0",
        "title": "Spain Ramps Up Pressure on Apple, Amazon in Yearslong Antitrust Case",
        "published": 1772027400,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260225006487:0-spain-ramps-up-pressure-on-apple-amazon-in-yearslong-antitrust-case/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L8N3ZL16B:0",
        "title": "Spain's antitrust watchdog says Apple, Amazon took too long to refine anti-competitive contracts",
        "published": 1772025565,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L8N3ZL16B:0-spain-s-antitrust-watchdog-says-apple-amazon-took-too-long-to-refine-anti-competitive-contracts/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "stocktwits:7e7d034ba094b:0",
        "title": "Apple CEO Tim Cook ‘Slept With One Eye Open’ After CIA Secret Brief About China Possibly Striking Taiwan: Report",
        "published": 1771998942,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-ceo-tim-cook-slept-with-one-eye-open-after-cia-secret-brief-about-china-possibly-striking-taiwan/cZRUMiIR469",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:7e7d034ba094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_DN20260224014448:0",
        "title": "Review and Preview: On Claude Nine — Barrons.com",
        "published": 1771980480,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMD",
            "logoid": "advanced-micro-devices"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:LZ",
            "logoid": "legalzoom"
          },
          {
            "symbol": "NYSE:SNOW",
            "logoid": "snowflake"
          }
        ],
        "storyPath": "/news/DJN_DN20260224014448:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN3ZK1ES:0",
        "title": "Apple’s Touch-Screen Macbook Pro To Have Dynamic Island, New Interface - Bloomberg News",
        "published": 1771967467,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN3ZK1ES:0-apple-s-touch-screen-macbook-pro-to-have-dynamic-island-new-interface-bloomberg-news/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260224008928:0",
        "title": "Apple Vowed to Boost U.S. Manufacturing. The Mac Mini Will Be Built in This City. — Barrons.com",
        "published": 1771965600,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260224008928:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L4N3ZK1K3:0",
        "title": "Wall St rebounds from tech rout; tariff, AI worries linger",
        "published": 1771953683,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NYSE:CRM",
            "logoid": "salesforce"
          },
          {
            "symbol": "DJ:DJI",
            "logoid": "indices/dow-30"
          },
          {
            "symbol": "SP:SPX",
            "logoid": "indices/s-and-p-500"
          },
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "SP:SPF",
            "logoid": "sector/financial"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:AMD",
            "logoid": "advanced-micro-devices"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NYSE:HD",
            "logoid": "home-depot"
          },
          {
            "symbol": "NYSE:KEYS",
            "logoid": "keysight-technologies"
          },
          {
            "symbol": "TVC:DJI",
            "logoid": "indices/dow-30"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L4N3ZK1K3:0-wall-st-rebounds-from-tech-rout-tariff-ai-worries-linger/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      }
    ],
    "streaming": {
      "channel": "64e27170d46efffb047e96cec6c2"
    },
    "pagination": {
      "cursor": "eyJfaWQiOiJzdG9ja3R3aXRzOmI4ZWY4OTFmNTA5NGIiLCJwdWJkYXRlIjoxNzcxOTUxMjk3MDAwfQ=="
    }
  },
  "msg": "Success"
}
```

## Get Bond News

`GET /api/news/bond`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/api/news/bond?symbol=NASDAQ%3AAAPL&lang=en' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "leverage_shares:c4f7ba997094b:0",
        "title": "2 Markets 2 Different Tales",
        "published": 1697126697,
        "urgency": 2,
        "link": "https://leverageshares.com/en/insights/2-markets-2-different-tales/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:COIN",
            "logoid": "coinbase"
          },
          {
            "symbol": "NASDAQ:TQQQ",
            "logoid": "proshares"
          },
          {
            "symbol": "NASDAQ:QQQ",
            "logoid": "invesco"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "LSE:TLT5",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3SYE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:5STL",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:5SPY",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:5TLT",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "NASDAQ:SQQQ",
            "logoid": "proshares"
          },
          {
            "symbol": "NASDAQ:MRNA",
            "logoid": "moderna"
          },
          {
            "symbol": "LSE:SPY3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SSPY",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:5STL",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:TLT5",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SP5Y",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:KRON"
          },
          {
            "symbol": "XETR:SPL",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:5SPE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SSPE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:TL5S",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3SPY",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:SSPY",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:5SPE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SPYS",
            "logoid": "leverage-shares"
          }
        ],
        "storyPath": "/news/leverage_shares:c4f7ba997094b:0-2-markets-2-different-tales/",
        "provider": {
          "id": "leverage_shares",
          "name": "Leverage Shares",
          "logo_id": "leverage-shares",
          "url": "https://leverageshares.com/en/"
        }
      },
      {
        "id": "leverage_shares:1cbc6e181094b:0",
        "title": "The time for bonds is now",
        "published": 1686832868,
        "urgency": 2,
        "link": "https://leverageshares.com/en/insights/the-time-for-bonds-is-now/",
        "relatedSymbols": [
          {
            "symbol": "LSE:5TLT",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "LSE:1BRN",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:5STL",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAP1"
          },
          {
            "symbol": "LSE:SAPE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:1APS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:5STL",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAPS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:APLS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3AAP",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:3SAA",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:TLT5",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAP2",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:3APE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:1AAP"
          },
          {
            "symbol": "LSE:2AAP",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3SAA",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAP3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SAPL",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SALE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3APE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAPE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:TLT5",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:TL5S",
            "logoid": "leverage-shares"
          }
        ],
        "storyPath": "/news/leverage_shares:1cbc6e181094b:0-the-time-for-bonds-is-now/",
        "provider": {
          "id": "leverage_shares",
          "name": "Leverage Shares",
          "logo_id": "leverage-shares",
          "url": "https://leverageshares.com/en/"
        }
      },
      {
        "id": "leverage_shares:5763ac7d0094b:0",
        "title": "Bonds vs Equities and the Debt Deal: Is a Winter Coming?",
        "published": 1686031200,
        "urgency": 2,
        "link": "https://leverageshares.com/en/insights/bonds-vs-equities-and-the-debt-deal-is-a-winter-coming/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:QQQ",
            "logoid": "invesco"
          },
          {
            "symbol": "LSE:1BRN",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "NASDAQ:TQQQ",
            "logoid": "proshares"
          },
          {
            "symbol": "NASDAQ:SQQQ",
            "logoid": "proshares"
          },
          {
            "symbol": "XETR:3APE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAPE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:2AAP",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3APE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3AAP",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAP1"
          },
          {
            "symbol": "LSE:AAP2",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:1AAP"
          },
          {
            "symbol": "LSE:AAP3",
            "logoid": "leverage-shares"
          }
        ],
        "storyPath": "/news/leverage_shares:5763ac7d0094b:0-bonds-vs-equities-and-the-debt-deal-is-a-winter-coming/",
        "provider": {
          "id": "leverage_shares",
          "name": "Leverage Shares",
          "logo_id": "leverage-shares",
          "url": "https://leverageshares.com/en/"
        }
      }
    ],
    "streaming": {
      "channel": "6ad4500e3ef6a056ee4a96ba7c4c"
    }
  },
  "msg": "Success"
}
```

## Get Crypto News

`GET /api/news/crypto`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/api/news/crypto?symbol=BINANCE:BTCUSDT&lang=en' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "newsbtc:6e878a888094b:0",
        "title": "Bitcoin Price Wave Down To $40,000 Shows When The Bottom Will Begin",
        "published": 1777168854,
        "urgency": 2,
        "link": "https://www.newsbtc.com/news/bitcoin/bitcoin-price-wave-down-to-40000-shows-when-the-bottom-will-begin/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:6e878a888094b:0-bitcoin-price-wave-down-to-40-000-shows-when-the-bottom-will-begin/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "newsbtc:f30adc0bd094b:0",
        "title": "Bitcoin Setup Suggests Liquidity Hunt Before Next Directional Move",
        "published": 1777165218,
        "urgency": 2,
        "link": "https://www.newsbtc.com/news/bitcoin/bitcoin-next-directional-move/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:f30adc0bd094b:0-bitcoin-setup-suggests-liquidity-hunt-before-next-directional-move/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "beincrypto:740688040094b:0",
        "title": "California Man Gets 70 Months in Prison for $260 Million Crypto Scam",
        "published": 1777153272,
        "urgency": 2,
        "link": "https://beincrypto.com/california-crypto-scam-sentencing/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/beincrypto:740688040094b:0-california-man-gets-70-months-in-prison-for-260-million-crypto-scam/",
        "provider": {
          "id": "beincrypto",
          "name": "Beincrypto",
          "logo_id": "beincrypto",
          "url": "https://beincrypto.com/"
        }
      },
      {
        "id": "cointelegraph:d620b6497094b:0",
        "title": "Bitcoiners cast doubt on the US military's understanding of the network",
        "published": 1777145789,
        "urgency": 2,
        "link": "https://cointelegraph.com/news/bitcoiners-cast-doubt-us-military-bitcoin?utm_source=rss_feed&utm_medium=rss-trading-view&utm_campaign=rss_partner_inbound",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/cointelegraph:d620b6497094b:0-bitcoiners-cast-doubt-on-the-us-military-s-understanding-of-the-network/",
        "provider": {
          "id": "cointelegraph",
          "name": "Cointelegraph",
          "logo_id": "cointelegraph-en",
          "url": "https://cointelegraph.com"
        }
      },
      {
        "id": "stocktwits:af2b4c9b6094b:0",
        "title": "Galaxy CEO Mike Novogratz Warns Saylor’s Bitcoin Buying Spree Could Trigger Supply Shock",
        "published": 1777138001,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/cryptocurrency/galaxy-ceo-saylor-bitcoin-buying-supply-shock/cZBK1RQRe2G",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "NASDAQ:MSTR",
            "logoid": "strategy-cad-hedged-cibc-cdr"
          }
        ],
        "storyPath": "/news/stocktwits:af2b4c9b6094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "beincrypto:57244ac65094b:0",
        "title": "Bitcoin Has 1 Week to Secure Its Best April Since 2020",
        "published": 1777136229,
        "urgency": 2,
        "link": "https://beincrypto.com/bitcoin-on-route-for-best-april-monthly-returns/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/beincrypto:57244ac65094b:0-bitcoin-has-1-week-to-secure-its-best-april-since-2020/",
        "provider": {
          "id": "beincrypto",
          "name": "Beincrypto",
          "logo_id": "beincrypto",
          "url": "https://beincrypto.com/"
        }
      },
      {
        "id": "cointelegraph:3e64fcc89094b:0",
        "title": "Bitcoin traders eye $73K next as weekly trend line holds price hostage",
        "published": 1777119737,
        "urgency": 2,
        "link": "https://cointelegraph.com/markets/bitcoin-traders-eye-73k-next-weekly-trend-line-holds-price-hostage?utm_source=rss_feed&utm_medium=rss-trading-view_BTC&utm_campaign=rss_partner_inbound",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/cointelegraph:3e64fcc89094b:0-bitcoin-traders-eye-73k-next-as-weekly-trend-line-holds-price-hostage/",
        "provider": {
          "id": "cointelegraph",
          "name": "Cointelegraph",
          "logo_id": "cointelegraph-en",
          "url": "https://cointelegraph.com"
        }
      },
      {
        "id": "newsbtc:ce62894e5094b:0",
        "title": "Bitcoin ‘Sharks’ Silently Accumulate Amid Market Uncertainty — Details",
        "published": 1777116654,
        "urgency": 2,
        "link": "https://www.newsbtc.com/news/bitcoin/bitcoin-sharks-silently-accumulate-amid-market-uncertainty-details/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:ce62894e5094b:0-bitcoin-sharks-silently-accumulate-amid-market-uncertainty-details/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "stocktwits:18023f3f8094b:0",
        "title": "VanEck Sees Bullish Shift In Bitcoin While Funding Rates Slide To Lowest Since 2023",
        "published": 1777113669,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/cryptocurrency/vaneck-sees-bullish-shift-in-bitcoin/cZBKII6Recx",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/stocktwits:18023f3f8094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "newsbtc:ca8f0507f094b:0",
        "title": "Bitcoin’s Big Players Are Accumulating — Is $80K Just The Start?",
        "published": 1777111216,
        "urgency": 2,
        "link": "https://www.newsbtc.com/news/bitcoin/bitcoins-big-players-are-accumulating-is-80k-just-the-start/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:ca8f0507f094b:0-bitcoin-s-big-players-are-accumulating-is-80k-just-the-start/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "cointelegraph:2694f3664094b:0",
        "title": "Spot Bitcoin ETFs see 9-day inflow streak as investors show resilience",
        "published": 1777106146,
        "urgency": 2,
        "link": "https://cointelegraph.com/news/spot-bitcoin-etfs-see-9-day-inflow-streak-as-investors-show-resilience?utm_source=rss_feed&utm_medium=rss-trading-view&utm_campaign=rss_partner_inbound",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/cointelegraph:2694f3664094b:0-spot-bitcoin-etfs-see-9-day-inflow-streak-as-investors-show-resilience/",
        "provider": {
          "id": "cointelegraph",
          "name": "Cointelegraph",
          "logo_id": "cointelegraph-en",
          "url": "https://cointelegraph.com"
        }
      },
      {
        "id": "newsbtc:869306e68094b:0",
        "title": "Bitcoin Traders Double Down On Bearish Bets Amid Consolidation – What This Means For Price",
        "published": 1777105830,
        "urgency": 2,
        "link": "https://www.newsbtc.com/news/bitcoin/bitcoin-traders-double-down-on-bearish-bets-amid-consolidation-what-this-means-for-price/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:869306e68094b:0-bitcoin-traders-double-down-on-bearish-bets-amid-consolidation-what-this-means-for-price/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "newsbtc:ad85556de094b:0",
        "title": "Bitcoin ETFs See Best Streak Since October 2025 As Inflows Hit $2.4B",
        "published": 1777093252,
        "urgency": 2,
        "link": "https://www.newsbtc.com/news/bitcoin/bitcoin-etfs-best-streak-october-2025-inflows/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:ad85556de094b:0-bitcoin-etfs-see-best-streak-since-october-2025-as-inflows-hit-2-4b/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "cointelegraph:168c408b6094b:0",
        "title": "Hyperliquid whale holds $38M short against Bitcoin, but does it matter?",
        "published": 1777084518,
        "urgency": 2,
        "link": "https://cointelegraph.com/markets/hyperliquid-whale-holds-38m-short-against-bitcoin-but-does-it-matter?utm_source=rss_feed&utm_medium=rss-trading-view_ETH&utm_campaign=rss_partner_inbound",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/cointelegraph:168c408b6094b:0-hyperliquid-whale-holds-38m-short-against-bitcoin-but-does-it-matter/",
        "provider": {
          "id": "cointelegraph",
          "name": "Cointelegraph",
          "logo_id": "cointelegraph-en",
          "url": "https://cointelegraph.com"
        }
      },
      {
        "id": "newsbtc:bee963ae1094b:0",
        "title": "Peter Brandt Sees Bitcoin Hitting $300,000-$500,000 By Late 2029",
        "published": 1777082411,
        "urgency": 2,
        "link": "https://www.newsbtc.com/bitcoin-news/peter-brandt-bitcoin-300000-500000/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:bee963ae1094b:0-peter-brandt-sees-bitcoin-hitting-300-000-500-000-by-late-2029/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "DJN_DN20260417000714:0",
        "title": "3 Things That Could Turn Crypto Around — Barron's",
        "published": 1777080660,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "BITSTAMP:ETHUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCETH"
          }
        ],
        "storyPath": "/news/DJN_DN20260417000714:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "beincrypto:097eec947094b:0",
        "title": "New Quantum Break Claim Sparks Bitcoin Security Debate",
        "published": 1777078887,
        "urgency": 2,
        "link": "https://beincrypto.com/quantum-bitcoin-break-claim-debate-crypto-security/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/beincrypto:097eec947094b:0-new-quantum-break-claim-sparks-bitcoin-security-debate/",
        "provider": {
          "id": "beincrypto",
          "name": "Beincrypto",
          "logo_id": "beincrypto",
          "url": "https://beincrypto.com/"
        }
      },
      {
        "id": "newsbtc:12cc251b3094b:0",
        "title": "Bitcoin Sentiment Warning: Social Media FOMO Spikes Again",
        "published": 1777078855,
        "urgency": 2,
        "link": "https://www.newsbtc.com/bitcoin-news/bitcoin-sentiment-warning-social-media-fomo/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:12cc251b3094b:0-bitcoin-sentiment-warning-social-media-fomo-spikes-again/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "u_today:2187ea4a5094b:0",
        "title": "Shiba Inu (SHIB): Everything Is Clear Now, Bitcoin's (BTC) Real Resistance Is $82,000, Another Dogecoin (DOGE) Zero Removal: Crypto Market Review",
        "published": 1777075260,
        "urgency": 2,
        "link": "https://u.today/shiba-inu-shib-everything-is-clear-now-bitcoins-btc-real-resistance-is-82000-another-dogecoin-doge",
        "relatedSymbols": [
          {
            "symbol": "COINBASE:SHIBUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCSHIB"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "CAPITALCOM:DOGEUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCDOGE"
          }
        ],
        "storyPath": "/news/u_today:2187ea4a5094b:0-shiba-inu-shib-everything-is-clear-now-bitcoin-s-btc-real-resistance-is-82-000-another-dogecoin-doge-zero-removal-crypto-market-review/",
        "provider": {
          "id": "u_today",
          "name": "U.Today",
          "logo_id": "u-today",
          "url": "https://u.today"
        }
      },
      {
        "id": "newsbtc:947fb67df094b:0",
        "title": "Bitcoin Funding Rates Stay Negative Despite Price Gains — What This Means",
        "published": 1777075210,
        "urgency": 2,
        "link": "https://www.newsbtc.com/news/bitcoin/bitcoin-funding-rates-negative/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:947fb67df094b:0-bitcoin-funding-rates-stay-negative-despite-price-gains-what-this-means/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "bravenewcoin:7aebc0bae094b:0",
        "title": "Quantum Computer Breaks Tiny Bitcoin-Style Key, and the Industry Should Stop Pretending This Is Just Sci-Fi",
        "published": 1777074917,
        "urgency": 2,
        "link": "https://bravenewcoin.com/insights/quantum-computer-breaks-tiny-bitcoin-style-key-and-the-industry-should-stop-pretending-this-is-just-sci-fi",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "BITSTAMP:ETHUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCETH"
          }
        ],
        "storyPath": "/news/bravenewcoin:7aebc0bae094b:0/",
        "provider": {
          "id": "bravenewcoin",
          "name": "Brave New Coin",
          "logo_id": "bravenewcoin",
          "url": "https://bravenewcoin.com/"
        }
      },
      {
        "id": "coinpedia:8c9fd82f1094b:0",
        "title": "Quantum Break: Researcher Wins 1 BTC for Largest ECC Attack Ever",
        "published": 1777068934,
        "urgency": 2,
        "link": "https://coinpedia.org/news/quantum-break-researcher-wins-1-btc-for-largest-ecc-attack-ever/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/coinpedia:8c9fd82f1094b:0-quantum-break-researcher-wins-1-btc-for-largest-ecc-attack-ever/",
        "provider": {
          "id": "coinpedia",
          "name": "Coinpedia",
          "logo_id": "coinpedia",
          "url": "https://www.coinpedia.org/"
        }
      },
      {
        "id": "cointelegraph:ecd9e1072094b:0",
        "title": "Bitcoin developer Paul Sztorc announces BTC hard fork called eCash",
        "published": 1777067700,
        "urgency": 2,
        "link": "https://cointelegraph.com/news/bitcoin-dev-paul-sztorc-hard-fork-ecash?utm_source=rss_feed&utm_medium=rss-trading-view_BCH&utm_campaign=rss_partner_inbound",
        "relatedSymbols": [
          {
            "symbol": "BINANCE:BTCUSDT",
            "currency-logoid": "crypto/XTVCUSDT",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "BINANCE:BCHUSDT",
            "currency-logoid": "crypto/XTVCUSDT",
            "base-currency-logoid": "crypto/XTVCBCH"
          }
        ],
        "storyPath": "/news/cointelegraph:ecd9e1072094b:0-bitcoin-developer-paul-sztorc-announces-btc-hard-fork-called-ecash/",
        "provider": {
          "id": "cointelegraph",
          "name": "Cointelegraph",
          "logo_id": "cointelegraph-en",
          "url": "https://cointelegraph.com"
        }
      },
      {
        "id": "newsbtc:98387a7b0094b:0",
        "title": "Will Bitcoin Fill The $82K CME Gap? $10B Could Be Liquidated—But Bulls May Hate What Follows",
        "published": 1777064362,
        "urgency": 2,
        "link": "https://www.newsbtc.com/breaking-news-ticker/will-bitcoin-fill-the-82k-cme-gap-10b-could-be-liquidated-but-bulls-may-hate-what-follows/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:98387a7b0094b:0-will-bitcoin-fill-the-82k-cme-gap-10b-could-be-liquidated-but-bulls-may-hate-what-follows/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "u_today:1fde1e316094b:0",
        "title": "'The O.C.' Star Lambasts Bitcoin on American TV",
        "published": 1777061985,
        "urgency": 2,
        "link": "https://u.today/the-oc-star-lambasts-bitcoin-on-american-tv",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/u_today:1fde1e316094b:0-the-o-c-star-lambasts-bitcoin-on-american-tv/",
        "provider": {
          "id": "u_today",
          "name": "U.Today",
          "logo_id": "u-today",
          "url": "https://u.today"
        }
      },
      {
        "id": "newsbtc:70ade440d094b:0",
        "title": "Bitcoin Is Existing Exchanges At An Alarming Rate, But How Are BTC Investors Faring In Terms Of Profit?",
        "published": 1777057230,
        "urgency": 2,
        "link": "https://www.newsbtc.com/news/bitcoin/bitcoin-is-existing-exchanges/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:70ade440d094b:0-bitcoin-is-existing-exchanges-at-an-alarming-rate-but-how-are-btc-investors-faring-in-terms-of-profit/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "cointelegraph:1ee744ddb094b:0",
        "title": "Quantum computer breaks 15-bit elliptic curve cryptographic key",
        "published": 1777056838,
        "urgency": 2,
        "link": "https://cointelegraph.com/news/quantum-computer-bit-elliptic-curve-key?utm_source=rss_feed&utm_medium=rss-trading-view_BTC&utm_campaign=rss_partner_inbound",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/cointelegraph:1ee744ddb094b:0-quantum-computer-breaks-15-bit-elliptic-curve-cryptographic-key/",
        "provider": {
          "id": "cointelegraph",
          "name": "Cointelegraph",
          "logo_id": "cointelegraph-en",
          "url": "https://cointelegraph.com"
        }
      },
      {
        "id": "u_today:22de34291094b:0",
        "title": "'Something Has Changed': Novogratz Predicts Bitcoin's Next Massive Breakout",
        "published": 1777056456,
        "urgency": 2,
        "link": "https://u.today/something-has-changed-novogratz-predicts-bitcoins-next-massive-breakout",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/u_today:22de34291094b:0-something-has-changed-novogratz-predicts-bitcoin-s-next-massive-breakout/",
        "provider": {
          "id": "u_today",
          "name": "U.Today",
          "logo_id": "u-today",
          "url": "https://u.today"
        }
      },
      {
        "id": "DJN_DN20260424007404:0",
        "title": "Crypto Fear and Greed Index Slides Back to Neutral — Market Talk",
        "published": 1777051680,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "BINANCE:BTCUSDT",
            "currency-logoid": "crypto/XTVCUSDT",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "BITSTAMP:ETHUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCETH"
          },
          {
            "symbol": "BINANCE:ETHUSDT",
            "currency-logoid": "crypto/XTVCUSDT",
            "base-currency-logoid": "crypto/XTVCETH"
          }
        ],
        "storyPath": "/news/DJN_DN20260424007404:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "cointelegraph:8e452f5a0094b:0",
        "title": "Bitcoin stays 'stalled' at $78K as oil threatens new risk-asset squeeze",
        "published": 1777049744,
        "urgency": 2,
        "link": "https://cointelegraph.com/markets/bitcoin-stays-stalled-at-78k-as-oil-threatens-new-risk-asset-squeeze?utm_source=rss_feed&utm_medium=rss-trading-view&utm_campaign=rss_partner_inbound",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/cointelegraph:8e452f5a0094b:0-bitcoin-stays-stalled-at-78k-as-oil-threatens-new-risk-asset-squeeze/",
        "provider": {
          "id": "cointelegraph",
          "name": "Cointelegraph",
          "logo_id": "cointelegraph-en",
          "url": "https://cointelegraph.com"
        }
      },
      {
        "id": "coinpedia:d149b0104094b:0",
        "title": "Bitcoin Price Today: BTC Up 30% From February Lows, iS $100K Next?",
        "published": 1777049590,
        "urgency": 2,
        "link": "https://coinpedia.org/news/bitcoin-price-today-btc-up-30-from-february-lows-is-100k-next/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/coinpedia:d149b0104094b:0-bitcoin-price-today-btc-up-30-from-february-lows-is-100k-next/",
        "provider": {
          "id": "coinpedia",
          "name": "Coinpedia",
          "logo_id": "coinpedia",
          "url": "https://www.coinpedia.org/"
        }
      },
      {
        "id": "invezz:452206cdd094b:0",
        "title": "Bitcoin nears $80K as ETF inflows hit $2.4B in April",
        "published": 1777046433,
        "urgency": 2,
        "link": "https://invezz.com/news/2026/04/24/bitcoin-nears-80k-as-etf-inflows-hit-1-9b-in-seven-day-streak/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/invezz:452206cdd094b:0-bitcoin-nears-80k-as-etf-inflows-hit-2-4b-in-april/",
        "provider": {
          "id": "invezz",
          "name": "Invezz",
          "logo_id": "invezz",
          "url": "https://invezz.com/"
        }
      },
      {
        "id": "cointelegraph:18958c562094b:0",
        "title": "Nakamoto taps Bitwise and Kraken for Bitcoin options strategy to hedge risk",
        "published": 1777046197,
        "urgency": 2,
        "link": "https://cointelegraph.com/news/nakamoto-taps-bitwise-kraken-bitcoin-options-strategy-hedge-risk?utm_source=rss_feed&utm_medium=rss-trading-view_BTC&utm_campaign=rss_partner_inbound",
        "relatedSymbols": [
          {
            "symbol": "CRYPTO:NAKAUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCNAKA"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/cointelegraph:18958c562094b:0-nakamoto-taps-bitwise-and-kraken-for-bitcoin-options-strategy-to-hedge-risk/",
        "provider": {
          "id": "cointelegraph",
          "name": "Cointelegraph",
          "logo_id": "cointelegraph-en",
          "url": "https://cointelegraph.com"
        }
      },
      {
        "id": "DJN_DN20260424006530:0",
        "title": "Fallout From Hack Still Playing Out in DeFi Ecosystem — Market Talk",
        "published": 1777044420,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "BINANCE:BTCUSDT",
            "currency-logoid": "crypto/XTVCUSDT",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "BITSTAMP:ETHUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCETH"
          },
          {
            "symbol": "BINANCE:ETHUSDT",
            "currency-logoid": "crypto/XTVCUSDT",
            "base-currency-logoid": "crypto/XTVCETH"
          }
        ],
        "storyPath": "/news/DJN_DN20260424006530:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:6a0858eeb094b:0",
        "title": "‘Why Hold Dollars?’ Arthur Hayes Says That A Cracking Financial System Could Be Bullish For Bitcoin",
        "published": 1777044068,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/cryptocurrency/arthur-hayes-says-that-a-cracking-financial-system-is-bullish-for-bitcoin/cZBhIldRecO",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/stocktwits:6a0858eeb094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_DN20260424006201:0",
        "title": "Sticky Gains in Bitcoin May Be a Sign of Fundamental Turn — Market Talk",
        "published": 1777042260,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/DJN_DN20260424006201:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "u_today:2579dd2ae094b:0",
        "title": "Adam Back Breaks Silence on 'Finding Satoshi' Doc, Says Timezone Gaps Debunk the Latest Bitcoin Creator Theory",
        "published": 1777038480,
        "urgency": 2,
        "link": "https://u.today/adam-back-breaks-silence-on-finding-satoshi-doc-says-timezone-gaps-debunk-the-latest-bitcoin",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/u_today:2579dd2ae094b:0-adam-back-breaks-silence-on-finding-satoshi-doc-says-timezone-gaps-debunk-the-latest-bitcoin-creator-theory/",
        "provider": {
          "id": "u_today",
          "name": "U.Today",
          "logo_id": "u-today",
          "url": "https://u.today"
        }
      },
      {
        "id": "chainwire:26d3557c2094b:0",
        "title": "Project Eleven Awards 1 BTC Q-Day Prize for Largest Quantum Attack on Elliptic Curve Cryptography to Date",
        "published": 1777037203,
        "urgency": 2,
        "link": "https://chainwire.org/2026/04/24/project-eleven-awards-1-btc-q-day-prize-for-largest-quantum-attack-on-elliptic-curve-cryptography-to-date/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/chainwire:26d3557c2094b:0-project-eleven-awards-1-btc-q-day-prize-for-largest-quantum-attack-on-elliptic-curve-cryptography-to-date/",
        "provider": {
          "id": "chainwire",
          "name": "Chainwire",
          "logo_id": "chainwire",
          "url": "https://www.chainwire.org"
        }
      },
      {
        "id": "stocktwits:812e3b3c6094b:0",
        "title": "Arthur Hayes Says Ethereum Could Get Bumped From The Top 3 By 2030 – But Not By Solana",
        "published": 1777036564,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/cryptocurrency/arthur-hayes-says-ethereum-could-get-out-from-the-top-3-by-2030/cZBh5eLRecd",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:ETHUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCETH"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/stocktwits:812e3b3c6094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "the_block:7443e49d5094b:0",
        "title": "Researcher breaks 15-bit elliptic curve key in ‘largest quantum attack,’ wins 1 bitcoin bounty from Project Eleven",
        "published": 1777035600,
        "urgency": 2,
        "link": "https://www.theblock.co/post/398792/researcher-breaks-15-bit-elliptic-curve-key-wins-1-bitcoin-bounty-project-eleven?utm_source=tradingview&utm_medium=rss",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/the_block:7443e49d5094b:0-researcher-breaks-15-bit-elliptic-curve-key-in-largest-quantum-attack-wins-1-bitcoin-bounty-from-project-eleven/",
        "provider": {
          "id": "the_block",
          "name": "The Block",
          "logo_id": "the-block",
          "url": "https://www.theblock.co/?utm_medium=rss&utm_source=tradingview"
        }
      },
      {
        "id": "cointelegraph:7e30ebfdf094b:0",
        "title": "Bitcoin price set for best gains since Q4 2024 with $77.5K monthly close",
        "published": 1777031505,
        "urgency": 2,
        "link": "https://cointelegraph.com/markets/bitcoin-price-set-for-best-gains-since-q4-2024-with-77-5k-monthly-close?utm_source=rss_feed&utm_medium=rss-trading-view&utm_campaign=rss_partner_inbound",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/cointelegraph:7e30ebfdf094b:0-bitcoin-price-set-for-best-gains-since-q4-2024-with-77-5k-monthly-close/",
        "provider": {
          "id": "cointelegraph",
          "name": "Cointelegraph",
          "logo_id": "cointelegraph-en",
          "url": "https://cointelegraph.com"
        }
      },
      {
        "id": "coinpedia:3e39b183d094b:0",
        "title": "BTC’s Rally Was a Short Squeeze, Not Real Buying, CryptoQuant",
        "published": 1777031307,
        "urgency": 2,
        "link": "https://coinpedia.org/news/btcs-rally-was-a-short-squeeze-not-real-buying-cryptoquant/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/coinpedia:3e39b183d094b:0-btc-s-rally-was-a-short-squeeze-not-real-buying-cryptoquant/",
        "provider": {
          "id": "coinpedia",
          "name": "Coinpedia",
          "logo_id": "coinpedia",
          "url": "https://www.coinpedia.org/"
        }
      },
      {
        "id": "DJN_DN20260424004227:0",
        "title": "Bitcoin Turns Higher But Only Slightly Amid Iran War Uncertainties — Market Talk",
        "published": 1777030740,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/DJN_DN20260424004227:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "cointelegraph:580d11827094b:0",
        "title": "Metaplanet raises $50M in zero-interest bonds to buy more Bitcoin",
        "published": 1777030402,
        "urgency": 2,
        "link": "https://cointelegraph.com/news/metaplanet-issues-50-million-in-zero-coupon-bonds-to-buy-more-bitcoin?utm_source=rss_feed&utm_medium=rss-trading-view&utm_campaign=rss_partner_inbound",
        "relatedSymbols": [
          {
            "symbol": "TSE:3350",
            "logoid": "metaplanet"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/cointelegraph:580d11827094b:0-metaplanet-raises-50m-in-zero-interest-bonds-to-buy-more-bitcoin/",
        "provider": {
          "id": "cointelegraph",
          "name": "Cointelegraph",
          "logo_id": "cointelegraph-en",
          "url": "https://cointelegraph.com"
        }
      },
      {
        "id": "stocktwits:a0fe56900094b:0",
        "title": "MSTR Vs BTC – Michael Saylor-Backed Strategy Rises In Early Trade, But Bitcoin Holds Weekly Edge",
        "published": 1777029055,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/cryptocurrency/mstr-vs-btc-saylor-backed-strategy-up-but-bitcoin-holds-weekly-edge/cZBhbv6ReTx",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSTR",
            "logoid": "strategy-cad-hedged-cibc-cdr"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/stocktwits:a0fe56900094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "newsbtc:fea7dc1d1094b:0",
        "title": "Bitcoin Recovery May Not Arrive Until October, Scaramucci Says",
        "published": 1777024824,
        "urgency": 2,
        "link": "https://www.newsbtc.com/bitcoin-news/bitcoin-recovery-not-until-october-scaramucci/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:fea7dc1d1094b:0-bitcoin-recovery-may-not-arrive-until-october-scaramucci-says/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "the_block:be385a198094b:0",
        "title": "Spot bitcoin ETFs draw $2 billion in net inflows over 8-day positive streak",
        "published": 1777023150,
        "urgency": 2,
        "link": "https://www.theblock.co/post/398757/spot-bitcoin-etf-8-day-streak?utm_source=tradingview&utm_medium=rss",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/the_block:be385a198094b:0-spot-bitcoin-etfs-draw-2-billion-in-net-inflows-over-8-day-positive-streak/",
        "provider": {
          "id": "the_block",
          "name": "The Block",
          "logo_id": "the-block",
          "url": "https://www.theblock.co/?utm_medium=rss&utm_source=tradingview"
        }
      },
      {
        "id": "beincrypto:6f7948461094b:0",
        "title": "Are Bitcoin Whales Opportunists? On-Chain Data Reveals the Truth",
        "published": 1777022665,
        "urgency": 2,
        "link": "https://beincrypto.com/bitcoin-whales-buy-bounce-not-bottom/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "CAPITALCOM:EMA"
          }
        ],
        "storyPath": "/news/beincrypto:6f7948461094b:0-are-bitcoin-whales-opportunists-on-chain-data-reveals-the-truth/",
        "provider": {
          "id": "beincrypto",
          "name": "Beincrypto",
          "logo_id": "beincrypto",
          "url": "https://beincrypto.com/"
        }
      },
      {
        "id": "u_today:1c6f667e9094b:0",
        "title": "Major Bitcoin Miner Keeps Cashing Out Bitcoin (BTC)",
        "published": 1777017407,
        "urgency": 2,
        "link": "https://u.today/major-bitcoin-miner-keeps-cashing-out-bitcoin-btc",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:RIOT",
            "logoid": "riot-blockchain"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/u_today:1c6f667e9094b:0-major-bitcoin-miner-keeps-cashing-out-bitcoin-btc/",
        "provider": {
          "id": "u_today",
          "name": "U.Today",
          "logo_id": "u-today",
          "url": "https://u.today"
        }
      },
      {
        "id": "beincrypto:333b1627f094b:0",
        "title": "Nearly $10 Billion April Options Expiry Puts Bitcoin and Ethereum Direction in Focus",
        "published": 1777016505,
        "urgency": 2,
        "link": "https://beincrypto.com/bitcoin-ethereum-options-expiry-april-2026/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "BITSTAMP:ETHUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCETH"
          }
        ],
        "storyPath": "/news/beincrypto:333b1627f094b:0-nearly-10-billion-april-options-expiry-puts-bitcoin-and-ethereum-direction-in-focus/",
        "provider": {
          "id": "beincrypto",
          "name": "Beincrypto",
          "logo_id": "beincrypto",
          "url": "https://beincrypto.com/"
        }
      },
      {
        "id": "the_block:eaaf2f709094b:0",
        "title": "Metaplanet issues $50 million in zero-interest bonds to buy more bitcoin",
        "published": 1777015082,
        "urgency": 2,
        "link": "https://www.theblock.co/post/398740/metaplanet-issues-bonds-bitcoin?utm_source=tradingview&utm_medium=rss",
        "relatedSymbols": [
          {
            "symbol": "TSE:3350",
            "logoid": "metaplanet"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/the_block:eaaf2f709094b:0-metaplanet-issues-50-million-in-zero-interest-bonds-to-buy-more-bitcoin/",
        "provider": {
          "id": "the_block",
          "name": "The Block",
          "logo_id": "the-block",
          "url": "https://www.theblock.co/?utm_medium=rss&utm_source=tradingview"
        }
      },
      {
        "id": "DJN_DN20260424001682:0",
        "title": "Bitcoin Falls as Iran War Uncertainty Keeps Investors Cautious — Market Talk",
        "published": 1777013760,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/DJN_DN20260424001682:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "coinpedia:c8b7dad90094b:0",
        "title": "Bitcoin News: Strategy CEO Maps 30% Yield Model, Calls it Future of Digital Credit",
        "published": 1777011951,
        "urgency": 2,
        "link": "https://coinpedia.org/news/bitcoin-news-strategy-ceo-maps-30-yield-model-calls-it-future-of-digital-credit/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSTR",
            "logoid": "strategy-cad-hedged-cibc-cdr"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/coinpedia:c8b7dad90094b:0-bitcoin-news-strategy-ceo-maps-30-yield-model-calls-it-future-of-digital-credit/",
        "provider": {
          "id": "coinpedia",
          "name": "Coinpedia",
          "logo_id": "coinpedia",
          "url": "https://www.coinpedia.org/"
        }
      },
      {
        "id": "u_today:942bbf11f094b:0",
        "title": "Spot Bitcoin ETFs Log $2.4B in Less Than Two Weeks",
        "published": 1777009602,
        "urgency": 2,
        "link": "https://u.today/spot-bitcoin-etfs-log-24b-in-less-than-two-weeks",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/u_today:942bbf11f094b:0-spot-bitcoin-etfs-log-2-4b-in-less-than-two-weeks/",
        "provider": {
          "id": "u_today",
          "name": "U.Today",
          "logo_id": "u-today",
          "url": "https://u.today"
        }
      },
      {
        "id": "beincrypto:22b958d41094b:0",
        "title": "Bitcoin Whales Accumulate 69% More BTC as ARK Warns the Bottom Isn’t In",
        "published": 1777008431,
        "urgency": 2,
        "link": "https://beincrypto.com/ark-bitcoin-bottom-whales-accumulation/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/beincrypto:22b958d41094b:0-bitcoin-whales-accumulate-69-more-btc-as-ark-warns-the-bottom-isn-t-in/",
        "provider": {
          "id": "beincrypto",
          "name": "Beincrypto",
          "logo_id": "beincrypto",
          "url": "https://beincrypto.com/"
        }
      },
      {
        "id": "newsbtc:865a5aad0094b:0",
        "title": "Bitcoin Enters Disbelief Phase As Traders Keep Shorting The Rally",
        "published": 1777006810,
        "urgency": 2,
        "link": "https://www.newsbtc.com/bitcoin-news/bitcoin-disbelief-phase-traders-keep-shorting-rally/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:865a5aad0094b:0-bitcoin-enters-disbelief-phase-as-traders-keep-shorting-the-rally/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "newsbtc:d82c73984094b:0",
        "title": "Analyst Predicts A 30% Bitcoin Price Crash To $50,000, Here’s When",
        "published": 1776999628,
        "urgency": 2,
        "link": "https://www.newsbtc.com/news/bitcoin/30-bitcoin-price-crash-50000/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:d82c73984094b:0-analyst-predicts-a-30-bitcoin-price-crash-to-50-000-here-s-when/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "newsbtc:100f56fc1094b:0",
        "title": "Bitcoin Price Strengthens, Fresh Upside Targets Come Into View",
        "published": 1776997854,
        "urgency": 2,
        "link": "https://www.newsbtc.com/analysis/btc/bitcoin-price-strengthens-78k/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:100f56fc1094b:0-bitcoin-price-strengthens-fresh-upside-targets-come-into-view/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "newsbtc:fbd618a29094b:0",
        "title": "$80K Bitcoin Target Back In Play As Trump Suggests US-Iran Talks Could Restart",
        "published": 1776996023,
        "urgency": 2,
        "link": "https://www.newsbtc.com/news/bitcoin/80k-bitcoin-target-back-in-play-as-trump-suggests-us-iran-talks-could-restart/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:fbd618a29094b:0-80k-bitcoin-target-back-in-play-as-trump-suggests-us-iran-talks-could-restart/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "cointelegraph:810567ff8094b:0",
        "title": "Critical Bitcoin trend change in works, but analysts say daily close above $80K required",
        "published": 1776995461,
        "urgency": 2,
        "link": "https://cointelegraph.com/markets/critical-bitcoin-trend-change-in-works-but-analysts-say-daily-close-above-dollar80k-required?utm_source=rss_feed&utm_medium=rss-trading-view_BTC&utm_campaign=rss_partner_inbound",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/cointelegraph:810567ff8094b:0-critical-bitcoin-trend-change-in-works-but-analysts-say-daily-close-above-80k-required/",
        "provider": {
          "id": "cointelegraph",
          "name": "Cointelegraph",
          "logo_id": "cointelegraph-en",
          "url": "https://cointelegraph.com"
        }
      },
      {
        "id": "bravenewcoin:2e0e1dd81094b:0",
        "title": "Bitcoin’s Rally Has Legs, But $80,000 Is Still the Line in the Sand",
        "published": 1776994935,
        "urgency": 2,
        "link": "https://bravenewcoin.com/insights/bitcoins-rally-has-legs-but-80000-is-still-the-line-in-the-sand",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/bravenewcoin:2e0e1dd81094b:0/",
        "provider": {
          "id": "bravenewcoin",
          "name": "Brave New Coin",
          "logo_id": "bravenewcoin",
          "url": "https://bravenewcoin.com/"
        }
      },
      {
        "id": "cointelegraph:9b9f1eb7d094b:0",
        "title": "Altcoins have ‘30% to 60%’ upside if Bitcoin taps $86K: Analyst",
        "published": 1776992977,
        "urgency": 2,
        "link": "https://cointelegraph.com/news/altcoins-upside-if-bitcoin-taps-86k-analyst?utm_source=rss_feed&utm_medium=rss-trading-view&utm_campaign=rss_partner_inbound",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          }
        ],
        "storyPath": "/news/cointelegraph:9b9f1eb7d094b:0-altcoins-have-30-to-60-upside-if-bitcoin-taps-86k-analyst/",
        "provider": {
          "id": "cointelegraph",
          "name": "Cointelegraph",
          "logo_id": "cointelegraph-en",
          "url": "https://cointelegraph.com"
        }
      },
      {
        "id": "newsbtc:4bcca3c5e094b:0",
        "title": "The Bitcoin Cycle Is Different: Crypto Expert Reveals When Price Will Cross $100,000 Again",
        "published": 1776988827,
        "urgency": 2,
        "link": "https://www.newsbtc.com/news/bitcoin/the-bitcoin-cycle-is-different/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:4bcca3c5e094b:0-the-bitcoin-cycle-is-different-crypto-expert-reveals-when-price-will-cross-100-000-again/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "cointelegraph:0346666a9094b:0",
        "title": "Global crypto adoption slumps amid macro pressures, Turkey defies downtrend",
        "published": 1776979296,
        "urgency": 2,
        "link": "https://cointelegraph.com/news/global-crypto-adoption-q1-2026-trm-labs-turkey-resilience?utm_source=rss_feed&utm_medium=rss-trading-view&utm_campaign=rss_partner_inbound",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/cointelegraph:0346666a9094b:0-global-crypto-adoption-slumps-amid-macro-pressures-turkey-defies-downtrend/",
        "provider": {
          "id": "cointelegraph",
          "name": "Cointelegraph",
          "logo_id": "cointelegraph-en",
          "url": "https://cointelegraph.com"
        }
      },
      {
        "id": "u_today:a736bba3d094b:0",
        "title": "Shiba Inu Sees 88% Surge in Usage, XRP Ledger to Break One Billion Threshold, BlackRock Buys $900 Million Worth of Bitcoin — U.Today Crypto Digest",
        "published": 1776978933,
        "urgency": 2,
        "link": "https://u.today/shiba-inu-sees-88-surge-in-usage-xrp-ledger-to-break-one-billion-threshold-blackrock-buys-900",
        "relatedSymbols": [
          {
            "symbol": "COINBASE:SHIBUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCSHIB"
          },
          {
            "symbol": "BITSTAMP:XRPUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCXRP"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/u_today:a736bba3d094b:0-shiba-inu-sees-88-surge-in-usage-xrp-ledger-to-break-one-billion-threshold-blackrock-buys-900-million-worth-of-bitcoin-u-today-crypto-digest/",
        "provider": {
          "id": "u_today",
          "name": "U.Today",
          "logo_id": "u-today",
          "url": "https://u.today"
        }
      },
      {
        "id": "u_today:23b9b6d59094b:0",
        "title": "Bitcoin Could Hit $500K, Veteran Trader Predicts",
        "published": 1776977463,
        "urgency": 2,
        "link": "https://u.today/bitcoin-could-hit-500k-veteran-trader-predicts",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/u_today:23b9b6d59094b:0-bitcoin-could-hit-500k-veteran-trader-predicts/",
        "provider": {
          "id": "u_today",
          "name": "U.Today",
          "logo_id": "u-today",
          "url": "https://u.today"
        }
      },
      {
        "id": "the_block:9119d42ff094b:0",
        "title": "Bitcoin ETF ‘flows turned positive for the year’: BNY’s global head of ETFs",
        "published": 1776974423,
        "urgency": 2,
        "link": "https://www.theblock.co/post/398699/bitcoin-etf-flows-turned-positive-year-bny-global-head-etfs?utm_source=tradingview&utm_medium=rss",
        "relatedSymbols": [
          {
            "symbol": "AMEX:GBTC",
            "logoid": "grayscale"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/the_block:9119d42ff094b:0-bitcoin-etf-flows-turned-positive-for-the-year-bny-s-global-head-of-etfs/",
        "provider": {
          "id": "the_block",
          "name": "The Block",
          "logo_id": "the-block",
          "url": "https://www.theblock.co/?utm_medium=rss&utm_source=tradingview"
        }
      },
      {
        "id": "cointelegraph:1b0dd53b2094b:0",
        "title": "Bitcoin enters disbelief phase as USDC exchange reserves push above $7.5B",
        "published": 1776972406,
        "urgency": 2,
        "link": "https://cointelegraph.com/markets/bitcoin-enters-disbelief-phase-as-usdc-exchange-reserves-push-above-dollar7-5b?utm_source=rss_feed&utm_medium=rss-trading-view_BTC&utm_campaign=rss_partner_inbound",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/cointelegraph:1b0dd53b2094b:0-bitcoin-enters-disbelief-phase-as-usdc-exchange-reserves-push-above-7-5b/",
        "provider": {
          "id": "cointelegraph",
          "name": "Cointelegraph",
          "logo_id": "cointelegraph-en",
          "url": "https://cointelegraph.com"
        }
      },
      {
        "id": "u_today:45f897c3b094b:0",
        "title": "Bitcoin (BTC) Price: Fidelity Predicts Next Major Wave",
        "published": 1776971917,
        "urgency": 2,
        "link": "https://u.today/bitcoin-btc-price-fidelity-predicts-next-major-wave",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/u_today:45f897c3b094b:0-bitcoin-btc-price-fidelity-predicts-next-major-wave/",
        "provider": {
          "id": "u_today",
          "name": "U.Today",
          "logo_id": "u-today",
          "url": "https://u.today"
        }
      },
      {
        "id": "newsbtc:ea359d753094b:0",
        "title": "Bitcoin Nears $80,000: Two Scenarios That May Decide Q2—Bulls Or Bears?",
        "published": 1776968743,
        "urgency": 2,
        "link": "https://www.newsbtc.com/breaking-news-ticker/bitcoin-nears-80000-two-scenarios-that-may-decide-q2-bulls-or-bears/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:ea359d753094b:0-bitcoin-nears-80-000-two-scenarios-that-may-decide-q2-bulls-or-bears/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "beincrypto:e6efe4f10094b:0",
        "title": "Senator Lummis Backs Bitcoin for US Cyber Defense After Admiral Paparo Testimony",
        "published": 1776967503,
        "urgency": 2,
        "link": "https://beincrypto.com/bitcoin-for-us-defense-cyber-defense/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/beincrypto:e6efe4f10094b:0-senator-lummis-backs-bitcoin-for-us-cyber-defense-after-admiral-paparo-testimony/",
        "provider": {
          "id": "beincrypto",
          "name": "Beincrypto",
          "logo_id": "beincrypto",
          "url": "https://beincrypto.com/"
        }
      },
      {
        "id": "DJN_DN20260423010534:0",
        "title": "Cryptocurrency Down as Middle East Tensions Persist — Market Talk",
        "published": 1776965940,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "BITSTAMP:ETHUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCETH"
          },
          {
            "symbol": "BITSTAMP:XRPUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCXRP"
          }
        ],
        "storyPath": "/news/DJN_DN20260423010534:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "bravenewcoin:d909c9ae3094b:0",
        "title": "Verifiable Bitcoin Accounts for Institutional Bitcoin. Your Custody, Your Terms.",
        "published": 1776965334,
        "urgency": 2,
        "link": "https://bravenewcoin.com/press-release/verifiable-bitcoin-accounts-for-institutional-bitcoin-your-custody-your-terms",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/bravenewcoin:d909c9ae3094b:0/",
        "provider": {
          "id": "bravenewcoin",
          "name": "Brave New Coin",
          "logo_id": "bravenewcoin",
          "url": "https://bravenewcoin.com/"
        }
      },
      {
        "id": "chainwire:7f8f00b4a094b:0",
        "title": "Verifiable Bitcoin Accounts for Institutional Bitcoin. Your Custody, Your Terms.",
        "published": 1776965064,
        "urgency": 2,
        "link": "https://chainwire.org/2026/04/23/verifiable-bitcoin-accounts-for-institutional-bitcoin-your-custody-your-terms/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/chainwire:7f8f00b4a094b:0-verifiable-bitcoin-accounts-for-institutional-bitcoin-your-custody-your-terms/",
        "provider": {
          "id": "chainwire",
          "name": "Chainwire",
          "logo_id": "chainwire",
          "url": "https://www.chainwire.org"
        }
      },
      {
        "id": "DJN_DN20260423010149:0",
        "title": "Stablecoins Enter Third Stage of Evolution, Says CoinDesk — Market Talk",
        "published": 1776962820,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "BITSTAMP:ETHUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCETH"
          }
        ],
        "storyPath": "/news/DJN_DN20260423010149:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "beincrypto:a7a585feb094b:0",
        "title": "Bitcoin’s $80,000 Target Remains Elusive Amid New US-China Tensions",
        "published": 1776961791,
        "urgency": 2,
        "link": "https://beincrypto.com/bitcoin-price-us-china-ai-tensions/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/beincrypto:a7a585feb094b:0-bitcoin-s-80-000-target-remains-elusive-amid-new-us-china-tensions/",
        "provider": {
          "id": "beincrypto",
          "name": "Beincrypto",
          "logo_id": "beincrypto",
          "url": "https://beincrypto.com/"
        }
      },
      {
        "id": "DJN_DN20260423009175:0",
        "title": "CLARITY Act Seen Critical in Maturation of Blockchain Tech — Market Talk",
        "published": 1776958920,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:ETHUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCETH"
          },
          {
            "symbol": "BINANCE:ETHUSDT",
            "currency-logoid": "crypto/XTVCUSDT",
            "base-currency-logoid": "crypto/XTVCETH"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "BINANCE:BTCUSDT",
            "currency-logoid": "crypto/XTVCUSDT",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/DJN_DN20260423009175:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "cointelegraph:e6bed636f094b:0",
        "title": "Bitcoin weekly close in focus after BTC price fails to revisit $80K",
        "published": 1776957993,
        "urgency": 2,
        "link": "https://cointelegraph.com/markets/bitcoin-weekly-close-in-focus-after-btc-price-fails-to-revisit-80k?utm_source=rss_feed&utm_medium=rss-trading-view_BTC&utm_campaign=rss_partner_inbound",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/cointelegraph:e6bed636f094b:0-bitcoin-weekly-close-in-focus-after-btc-price-fails-to-revisit-80k/",
        "provider": {
          "id": "cointelegraph",
          "name": "Cointelegraph",
          "logo_id": "cointelegraph-en",
          "url": "https://cointelegraph.com"
        }
      },
      {
        "id": "coinpedia:395582f6a094b:0",
        "title": "Bitwise Strategist Says XRP Is No Longer a Crypto Bet, It Is Fintech Infrastructure Now",
        "published": 1776957975,
        "urgency": 2,
        "link": "https://coinpedia.org/news/bitwise-strategist-says-xrp-is-no-longer-a-crypto-bet-it-is-fintech-infrastructure-now/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:XRPUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCXRP"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "BITSTAMP:ETHUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCETH"
          }
        ],
        "storyPath": "/news/coinpedia:395582f6a094b:0-bitwise-strategist-says-xrp-is-no-longer-a-crypto-bet-it-is-fintech-infrastructure-now/",
        "provider": {
          "id": "coinpedia",
          "name": "Coinpedia",
          "logo_id": "coinpedia",
          "url": "https://www.coinpedia.org/"
        }
      },
      {
        "id": "the_block:a9efdea2b094b:0",
        "title": "‘Rally on trial’: Bitcoin breakout faces key $80,000 test as whales, ETF investors buy into volatility",
        "published": 1776957856,
        "urgency": 2,
        "link": "https://www.theblock.co/post/398625/rally-trial-analysts-bitcoin-breakout-test-80000-whales-etf-investors-buy-volatility?utm_source=tradingview&utm_medium=rss",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/the_block:a9efdea2b094b:0-rally-on-trial-bitcoin-breakout-faces-key-80-000-test-as-whales-etf-investors-buy-into-volatility/",
        "provider": {
          "id": "the_block",
          "name": "The Block",
          "logo_id": "the-block",
          "url": "https://www.theblock.co/?utm_medium=rss&utm_source=tradingview"
        }
      },
      {
        "id": "cointelegraph:660eba3c3094b:0",
        "title": "Spain seizes crypto cold wallets in illegal manga piracy raid",
        "published": 1776956668,
        "urgency": 2,
        "link": "https://cointelegraph.com/news/spain-seizes-crypto-cold-wallets-manga-piracy?utm_source=rss_feed&utm_medium=rss-trading-view&utm_campaign=rss_partner_inbound",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/cointelegraph:660eba3c3094b:0-spain-seizes-crypto-cold-wallets-in-illegal-manga-piracy-raid/",
        "provider": {
          "id": "cointelegraph",
          "name": "Cointelegraph",
          "logo_id": "cointelegraph-en",
          "url": "https://cointelegraph.com"
        }
      },
      {
        "id": "DJN_DN20260423002588:0",
        "title": "Bitcoin Price Falls From 11-Week High. Why Ethereum, XRP, Cryptos Are Dropping. — Barrons.com",
        "published": 1776956340,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/DJN_DN20260423002588:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "coinpedia:445ebe98d094b:0",
        "title": "CoinEx Founder Yang Haipo Says Crypto’s Collapse Is Inevitable, And Numbers to Back It Up",
        "published": 1776952097,
        "urgency": 2,
        "link": "https://coinpedia.org/news/coinex-founder-yang-haipo-says-cryptos-collapse-is-inevitable-and-numbers-to-back-it-up/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/coinpedia:445ebe98d094b:0-coinex-founder-yang-haipo-says-crypto-s-collapse-is-inevitable-and-numbers-to-back-it-up/",
        "provider": {
          "id": "coinpedia",
          "name": "Coinpedia",
          "logo_id": "coinpedia",
          "url": "https://www.coinpedia.org/"
        }
      },
      {
        "id": "u_today:612e2ccce094b:0",
        "title": "Bitcoin Price Battle for $87,000: Peter Brandt Identifies the Final Hurdle in Current Rally",
        "published": 1776951300,
        "urgency": 2,
        "link": "https://u.today/bitcoin-price-battle-for-87000-peter-brandt-identifies-the-final-hurdle-in-current-rally",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/u_today:612e2ccce094b:0-bitcoin-price-battle-for-87-000-peter-brandt-identifies-the-final-hurdle-in-current-rally/",
        "provider": {
          "id": "u_today",
          "name": "U.Today",
          "logo_id": "u-today",
          "url": "https://u.today"
        }
      },
      {
        "id": "beincrypto:09e67d264094b:0",
        "title": "3 Warning Signs That Bitcoin’s Rally May Be At Risk",
        "published": 1776950912,
        "urgency": 2,
        "link": "https://beincrypto.com/bitcoin-rally-warning-signs-april-2026/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/beincrypto:09e67d264094b:0-3-warning-signs-that-bitcoin-s-rally-may-be-at-risk/",
        "provider": {
          "id": "beincrypto",
          "name": "Beincrypto",
          "logo_id": "beincrypto",
          "url": "https://beincrypto.com/"
        }
      },
      {
        "id": "stocktwits:a12909fb9094b:0",
        "title": "Crypto Is A Casino – Bitcoin's Collapse Is ‘Inevitable’ As Transfusions Run Out, Says Industry Insider",
        "published": 1776950129,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/cryptocurrency/crypto-is-a-casino-bitcoin-collapse-is-inevitable-as-transfusions-run-out/cZBfUT4ReRO",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/stocktwits:a12909fb9094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "the_block:597b33696094b:0",
        "title": "US military running Bitcoin node to test national security applications, admiral tells Congress",
        "published": 1776949741,
        "urgency": 2,
        "link": "https://www.theblock.co/post/398593/us-military-running-bitcoin-node-to-test-national-security-applications-admiral-tells-congress?utm_source=tradingview&utm_medium=rss",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/the_block:597b33696094b:0-us-military-running-bitcoin-node-to-test-national-security-applications-admiral-tells-congress/",
        "provider": {
          "id": "the_block",
          "name": "The Block",
          "logo_id": "the-block",
          "url": "https://www.theblock.co/?utm_medium=rss&utm_source=tradingview"
        }
      },
      {
        "id": "the_block:5a88076ca094b:0",
        "title": "Pantera among investors pushing bitcoin treasury firm Satsuma to sell $50 million hoard: Bloomberg",
        "published": 1776949483,
        "urgency": 2,
        "link": "https://www.theblock.co/post/398590/pantera-among-investors-pushing-bitcoin-treasury-firm-satsuma-to-sell-50-million-hoard-bloomberg?utm_source=tradingview&utm_medium=rss",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/the_block:5a88076ca094b:0-pantera-among-investors-pushing-bitcoin-treasury-firm-satsuma-to-sell-50-million-hoard-bloomberg/",
        "provider": {
          "id": "the_block",
          "name": "The Block",
          "logo_id": "the-block",
          "url": "https://www.theblock.co/?utm_medium=rss&utm_source=tradingview"
        }
      },
      {
        "id": "newsbtc:8c1185c38094b:0",
        "title": "Bitcoin To $140,000 And XRP To $7? Here’s When It Will Happen",
        "published": 1776947405,
        "urgency": 2,
        "link": "https://www.newsbtc.com/bitcoin-news/bitcoin-140000-and-xrp-7/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "BITSTAMP:XRPUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCXRP"
          }
        ],
        "storyPath": "/news/newsbtc:8c1185c38094b:0-bitcoin-to-140-000-and-xrp-to-7-here-s-when-it-will-happen/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "stocktwits:1d388e52b094b:0",
        "title": "Bitcoin’s $80K Problem Ahead: Over Half Of Short-Term BTC Holders Are About To Hit A Profit Zone",
        "published": 1776945803,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/cryptocurrency/bitcoin-is-burning-4-4-million-in-profit-every-hour-warning-sign/cZBfwdiReRI",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/stocktwits:1d388e52b094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_DN20260423006464:0",
        "title": "Bitcoin Eases Further as Iran War Tensions Weigh — Market Talk",
        "published": 1776945780,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "BINANCE:BTCUSDT",
            "currency-logoid": "crypto/XTVCUSDT",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/DJN_DN20260423006464:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "cointelegraph:5f4db5d1b094b:0",
        "title": "BlackRock drives 7-day Bitcoin ETF inflow streak as BTC nears $80,000",
        "published": 1776945343,
        "urgency": 2,
        "link": "https://cointelegraph.com/news/bitcoin-etf-1-9-billiow-7-day-inflow-streak-btc-near-80k?utm_source=rss_feed&utm_medium=rss-trading-view_BTC&utm_campaign=rss_partner_inbound",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "BITSTAMP:ETHUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCETH"
          }
        ],
        "storyPath": "/news/cointelegraph:5f4db5d1b094b:0-blackrock-drives-7-day-bitcoin-etf-inflow-streak-as-btc-nears-80-000/",
        "provider": {
          "id": "cointelegraph",
          "name": "Cointelegraph",
          "logo_id": "cointelegraph-en",
          "url": "https://cointelegraph.com"
        }
      },
      {
        "id": "beincrypto:49590876e094b:0",
        "title": "Tesla Holds 11,509 BTC Untouched While Injecting $2 Billion Into SpaceX",
        "published": 1776944565,
        "urgency": 2,
        "link": "https://beincrypto.com/tesla-bitcoin-untouched-spacex-2b-q1/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          }
        ],
        "storyPath": "/news/beincrypto:49590876e094b:0-tesla-holds-11-509-btc-untouched-while-injecting-2-billion-into-spacex/",
        "provider": {
          "id": "beincrypto",
          "name": "Beincrypto",
          "logo_id": "beincrypto",
          "url": "https://beincrypto.com/"
        }
      },
      {
        "id": "cointelegraph:7f97a027a094b:0",
        "title": "Bitcoin buyers show ‘renewed conviction’ with BTC price push toward $79K",
        "published": 1776942961,
        "urgency": 2,
        "link": "https://cointelegraph.com/markets/bitcoin-buyers-renewed-conviction-btc-price-push-toward-79k?utm_source=rss_feed&utm_medium=rss-trading-view_BTC&utm_campaign=rss_partner_inbound",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/cointelegraph:7f97a027a094b:0-bitcoin-buyers-show-renewed-conviction-with-btc-price-push-toward-79k/",
        "provider": {
          "id": "cointelegraph",
          "name": "Cointelegraph",
          "logo_id": "cointelegraph-en",
          "url": "https://cointelegraph.com"
        }
      },
      {
        "id": "stocktwits:aaa2c5f68094b:0",
        "title": "Tesla Held Onto Its Bitcoin Stash In Q1 Despite Taking A $178M Tax Hit – TSLA Stock Slides Pre-Market",
        "published": 1776942306,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/tesla-held-onto-its-bitcoin-in-q1-taking-a-178-m-hit-tsla-stock-slides/cZBfuZPReRR",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/stocktwits:aaa2c5f68094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "coinpedia:0a2bca86b094b:0",
        "title": "Why Bitcoin Price Stuck at $79K, Michael van de Poppe Explains",
        "published": 1776938577,
        "urgency": 2,
        "link": "https://coinpedia.org/news/why-bitcoin-price-stuck-at-79k-michael-van-de-poppe-explains/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/coinpedia:0a2bca86b094b:0-why-bitcoin-price-stuck-at-79k-michael-van-de-poppe-explains/",
        "provider": {
          "id": "coinpedia",
          "name": "Coinpedia",
          "logo_id": "coinpedia",
          "url": "https://www.coinpedia.org/"
        }
      },
      {
        "id": "newsbtc:38f289adc094b:0",
        "title": "Next Big Bitcoin Move May Defy Everything Traders Expect, Says Expert",
        "published": 1776938440,
        "urgency": 2,
        "link": "https://www.newsbtc.com/bitcoin-news/next-big-bitcoin-defy-everything-traders-expect/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:38f289adc094b:0-next-big-bitcoin-move-may-defy-everything-traders-expect-says-expert/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "beincrypto:abb392b46094b:0",
        "title": "Adam Back Calls ‘Finding Satoshi’ Documentary’s Finney-Sassaman Theory ‘Odd’",
        "published": 1776936905,
        "urgency": 2,
        "link": "https://beincrypto.com/adam-back-finding-satoshi-finney-sassaman/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/beincrypto:abb392b46094b:0-adam-back-calls-finding-satoshi-documentary-s-finney-sassaman-theory-odd/",
        "provider": {
          "id": "beincrypto",
          "name": "Beincrypto",
          "logo_id": "beincrypto",
          "url": "https://beincrypto.com/"
        }
      },
      {
        "id": "DJN_DN20260423003319:0",
        "title": "Fresh Iran War Concerns Trigger Profit-Taking in Bitcoin — Market Talk",
        "published": 1776935880,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "BINANCE:BTCUSDT",
            "currency-logoid": "crypto/XTVCUSDT",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/DJN_DN20260423003319:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "u_today:9a207c930094b:0",
        "title": "Bitcoin (BTC) Price Is Bottoming, Says Expert Amid Enormous Short Orders Piling",
        "published": 1776933600,
        "urgency": 2,
        "link": "https://u.today/bitcoin-btc-price-is-bottoming-says-expert-amid-enormous-short-orders-piling",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/u_today:9a207c930094b:0-bitcoin-btc-price-is-bottoming-says-expert-amid-enormous-short-orders-piling/",
        "provider": {
          "id": "u_today",
          "name": "U.Today",
          "logo_id": "u-today",
          "url": "https://u.today"
        }
      },
      {
        "id": "newsbtc:41cb5da6d094b:0",
        "title": "Bitcoin Bull Cycle Is Right On Schedule: Analyst Reveals When The Bull Run Will Begin",
        "published": 1776933019,
        "urgency": 2,
        "link": "https://www.newsbtc.com/news/bitcoin/bitcoin-bull-cycle-on-schedule/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:41cb5da6d094b:0-bitcoin-bull-cycle-is-right-on-schedule-analyst-reveals-when-the-bull-run-will-begin/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "coinpedia:9bbfde684094b:0",
        "title": "Bitcoin Price Jumps Above $78K as Strong Demand Returns: Breakout Ahead?",
        "published": 1776932331,
        "urgency": 2,
        "link": "https://coinpedia.org/price-analysis/bitcoin-price-jumps-above-78k-as-strong-demand-returns-breakout-ahead/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/coinpedia:9bbfde684094b:0-bitcoin-price-jumps-above-78k-as-strong-demand-returns-breakout-ahead/",
        "provider": {
          "id": "coinpedia",
          "name": "Coinpedia",
          "logo_id": "coinpedia",
          "url": "https://www.coinpedia.org/"
        }
      },
      {
        "id": "u_today:878bc4819094b:0",
        "title": "Why Satoshi’s Identity No Longer Matters: Strategy and Coinbase CEOs Signal the End of the Hunt",
        "published": 1776932055,
        "urgency": 2,
        "link": "https://u.today/why-satoshis-identity-no-longer-matters-strategy-and-coinbase-ceos-signal-the-end-of-the-hunt",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/u_today:878bc4819094b:0-why-satoshi-s-identity-no-longer-matters-strategy-and-coinbase-ceos-signal-the-end-of-the-hunt/",
        "provider": {
          "id": "u_today",
          "name": "U.Today",
          "logo_id": "u-today",
          "url": "https://u.today"
        }
      },
      {
        "id": "forexlive:f722a4ceb094b:0",
        "title": "The single chart for bitcoin long term investors shows bulls are fine",
        "published": 1776931432,
        "urgency": 2,
        "link": "https://investinglive.com/Cryptocurrency/the-single-chart-that-for-bitcoin-long-term-investors-shows-bulls-are-fine-20260423/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/forexlive:f722a4ceb094b:0-the-single-chart-for-bitcoin-long-term-investors-shows-bulls-are-fine/",
        "provider": {
          "id": "forexlive",
          "name": "InvestingLive",
          "logo_id": "forexlive",
          "url": "https://www.investinglive.com/"
        }
      },
      {
        "id": "DJN_DN20260423002489:0",
        "title": "Bitcoin Consolidating Gains in Range-Compression Phase — Market Talk",
        "published": 1776930180,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/DJN_DN20260423002489:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "cointelegraph:e51e1fe34094b:0",
        "title": "Crypto sentiment index soars to a 3-month high as Bitcoin holds $77K",
        "published": 1776928031,
        "urgency": 2,
        "link": "https://cointelegraph.com/news/crypto-market-sentiment-hits-3-month-high?utm_source=rss_feed&utm_medium=rss-trading-view&utm_campaign=rss_partner_inbound",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/cointelegraph:e51e1fe34094b:0-crypto-sentiment-index-soars-to-a-3-month-high-as-bitcoin-holds-77k/",
        "provider": {
          "id": "cointelegraph",
          "name": "Cointelegraph",
          "logo_id": "cointelegraph-en",
          "url": "https://cointelegraph.com"
        }
      },
      {
        "id": "newsbtc:185c5e928094b:0",
        "title": "Bitcoin Rally Catches Shorts Offside—$200M Liquidated As Price Hits $79,000",
        "published": 1776927650,
        "urgency": 2,
        "link": "https://www.newsbtc.com/bitcoin-news/bitcoin-catches-shorts-200m-liquidated-price-79000/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:185c5e928094b:0-bitcoin-rally-catches-shorts-offside-200m-liquidated-as-price-hits-79-000/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "DJN_DN20260423002162:0",
        "title": "Bitcoin Turns Lower as Hopes For Iran War De-escalation Fade — Market Talk",
        "published": 1776927600,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "BINANCE:BTCUSDT",
            "currency-logoid": "crypto/XTVCUSDT",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/DJN_DN20260423002162:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_TUCBQMP78:0",
        "title": "Bluebird Mining Ventures To Invest In 4.8MW Bitcoin Mining Project In Texas",
        "published": 1776925619,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "LSE:BMV",
            "logoid": "bluebird-mining-ventures-ltd-ord-npv-di"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_TUCBQMP78:0-bluebird-mining-ventures-to-invest-in-4-8mw-bitcoin-mining-project-in-texas/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260423001824:0",
        "title": "Bitcoin in Uptrend That May Test $80,000, Technical Analysis Shows — Market Talk",
        "published": 1776924660,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/DJN_DN20260423001824:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "modular_finance:f5488d91a1da6:0",
        "title": "H100 signs binding agreement to increase bitcoin holdings to approximately 3,500 bitcoin",
        "published": 1776924000,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NGM:H100",
            "logoid": "h100"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/modular_finance:f5488d91a1da6:0-h100-signs-binding-agreement-to-increase-bitcoin-holdings-to-approximately-3-500-bitcoin/",
        "provider": {
          "id": "modular_finance",
          "name": "MFN by Modular Finance",
          "logo_id": "rdp-mfn",
          "url": "https://modularfinance.com"
        }
      },
      {
        "id": "invezz:60e5d796c094b:0",
        "title": "Thailand SEC proposes simpler licensing for crypto derivatives market",
        "published": 1776921152,
        "urgency": 2,
        "link": "https://invezz.com/news/2026/04/23/thailand-sec-proposes-simpler-licensing-route-for-crypto-derivatives-market/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/invezz:60e5d796c094b:0-thailand-sec-proposes-simpler-licensing-for-crypto-derivatives-market/",
        "provider": {
          "id": "invezz",
          "name": "Invezz",
          "logo_id": "invezz",
          "url": "https://invezz.com/"
        }
      },
      {
        "id": "newsbtc:3c19c4ee9094b:0",
        "title": "Bitcoin Watch: All Eyes On $86,000—What Could Fuel The Next Bullish Breakout",
        "published": 1776920451,
        "urgency": 2,
        "link": "https://www.newsbtc.com/bitcoin-news/bitcoin-watch-all-eyes-on-86000-what-could-fuel-the-next-bullish-breakout/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:3c19c4ee9094b:0-bitcoin-watch-all-eyes-on-86-000-what-could-fuel-the-next-bullish-breakout/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "coinpedia:7e1c1f0c7094b:0",
        "title": "Traders Bet on $100K Bitcoin Price as Breakout Rally Erases Weeks of Sideways Pain",
        "published": 1776920351,
        "urgency": 2,
        "link": "https://coinpedia.org/news/traders-bet-on-100k-bitcoin-price-as-breakout-rally-erases-weeks-of-sideways-pain/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/coinpedia:7e1c1f0c7094b:0-traders-bet-on-100k-bitcoin-price-as-breakout-rally-erases-weeks-of-sideways-pain/",
        "provider": {
          "id": "coinpedia",
          "name": "Coinpedia",
          "logo_id": "coinpedia",
          "url": "https://www.coinpedia.org/"
        }
      },
      {
        "id": "cryptobriefing:f733c7471094b:0",
        "title": "Tesla confirms no Bitcoin sales in Q1 despite market selloff",
        "published": 1776917053,
        "urgency": 2,
        "link": "https://cryptobriefing.com/tesla-bitcoin-intact-strategy-q1-2026/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/cryptobriefing:f733c7471094b:0-tesla-confirms-no-bitcoin-sales-in-q1-despite-market-selloff/",
        "provider": {
          "id": "cryptobriefing",
          "name": "Crypto Briefing",
          "logo_id": "crypto-briefing",
          "url": "https://cryptobriefing.com"
        }
      },
      {
        "id": "chainwire:268cf57dc094b:0",
        "title": "HashKey Group Announces Strategic Partnership with ANAP Holdings to Expand Bitcoin Treasury and Institutional Asset Management in Japan",
        "published": 1776916958,
        "urgency": 2,
        "link": "https://chainwire.org/2026/04/23/hashkey-group-announces-strategic-partnership-with-anap-holdings-to-expand-bitcoin-treasury-and-institutional-asset-management-in-japan/",
        "relatedSymbols": [
          {
            "symbol": "TSE:3189",
            "logoid": "anap"
          },
          {
            "symbol": "CRYPTO:HSKUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCHSK"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/chainwire:268cf57dc094b:0-hashkey-group-announces-strategic-partnership-with-anap-holdings-to-expand-bitcoin-treasury-and-institutional-asset-management-in-japan/",
        "provider": {
          "id": "chainwire",
          "name": "Chainwire",
          "logo_id": "chainwire",
          "url": "https://www.chainwire.org"
        }
      },
      {
        "id": "newsbtc:d070147b3094b:0",
        "title": "Bitcoin Hits $78,000—All Eyes On $80,700 Cost Basis?",
        "published": 1776916857,
        "urgency": 2,
        "link": "https://www.newsbtc.com/bitcoin-news/bitcoin-hits-78000-all-eyes-on-80700-cost-basis/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:d070147b3094b:0-bitcoin-hits-78-000-all-eyes-on-80-700-cost-basis/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "newsbtc:f9e3dece8094b:0",
        "title": "Consistent XRP Buys Could Deliver Outsized Gains By 2030: Finance Expert",
        "published": 1776913213,
        "urgency": 2,
        "link": "https://www.newsbtc.com/altcoin/consistent-xrp-buys-could-deliver-outsized-gains-by-2030-finance-expert/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:XRPUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCXRP"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:f9e3dece8094b:0-consistent-xrp-buys-could-deliver-outsized-gains-by-2030-finance-expert/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "newsbtc:cf0612fd8094b:0",
        "title": "Bitcoin Price Rally Nears $80K, Dips May Draw Fresh Buyers",
        "published": 1776911609,
        "urgency": 2,
        "link": "https://www.newsbtc.com/analysis/btc/bitcoin-price-rally-nears-80k/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:cf0612fd8094b:0-bitcoin-price-rally-nears-80k-dips-may-draw-fresh-buyers/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "newsbtc:534118ee3094b:0",
        "title": "Bitcoin Bulls Rebuild As Futures Metric Hits 4-Month High",
        "published": 1776909619,
        "urgency": 2,
        "link": "https://www.newsbtc.com/bitcoin-news/bitcoin-bulls-rebuild-futures-metric-4-month-high/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:534118ee3094b:0-bitcoin-bulls-rebuild-as-futures-metric-hits-4-month-high/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "cointelegraph:b15273bd7094b:0",
        "title": "LONGITUDE recap: Adam Back on Satoshi, crypto regulation needs tweaks",
        "published": 1776907834,
        "urgency": 2,
        "link": "https://cointelegraph.com/news/longitude-recap-adam-back-on-satoshi-crypto-regulation-needs-tweaks?utm_source=rss_feed&utm_medium=rss-trading-view&utm_campaign=rss_partner_inbound",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/cointelegraph:b15273bd7094b:0-longitude-recap-adam-back-on-satoshi-crypto-regulation-needs-tweaks/",
        "provider": {
          "id": "cointelegraph",
          "name": "Cointelegraph",
          "logo_id": "cointelegraph-en",
          "url": "https://cointelegraph.com"
        }
      },
      {
        "id": "cointelegraph:fc2df09e9094b:0",
        "title": "Four reasons why the crypto market is rallying today: Will bulls maintain control?",
        "published": 1776907800,
        "urgency": 2,
        "link": "https://cointelegraph.com/markets/four-reasons-why-the-crypto-market-is-rallying-today-will-bulls-maintain-control?utm_source=rss_feed&utm_medium=rss-trading-view_ETH&utm_campaign=rss_partner_inbound",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "BITSTAMP:ETHUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCETH"
          }
        ],
        "storyPath": "/news/cointelegraph:fc2df09e9094b:0-four-reasons-why-the-crypto-market-is-rallying-today-will-bulls-maintain-control/",
        "provider": {
          "id": "cointelegraph",
          "name": "Cointelegraph",
          "logo_id": "cointelegraph-en",
          "url": "https://cointelegraph.com"
        }
      },
      {
        "id": "cointelegraph:1e64b4d1a094b:0",
        "title": "Bitcoin chases monthly high above $80K as nearly all BTC price metrics turn bullish",
        "published": 1776904200,
        "urgency": 2,
        "link": "https://cointelegraph.com/markets/bitcoin-chases-monthly-high-above-dollar80k-as-nearly-all-btc-price-metrics-turn-bullish?utm_source=rss_feed&utm_medium=rss-trading-view_BTC&utm_campaign=rss_partner_inbound",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/cointelegraph:1e64b4d1a094b:0-bitcoin-chases-monthly-high-above-80k-as-nearly-all-btc-price-metrics-turn-bullish/",
        "provider": {
          "id": "cointelegraph",
          "name": "Cointelegraph",
          "logo_id": "cointelegraph-en",
          "url": "https://cointelegraph.com"
        }
      },
      {
        "id": "u_today:9b36e2fa5094b:0",
        "title": "Bitcoin (BTC) Closer to $80,000 Than $60,000 Again, Ethereum's (ETH) $3,000 Recipe, Hyperliquid (HYPE) Bounce Triggered: Crypto Market Review",
        "published": 1776902460,
        "urgency": 2,
        "link": "https://u.today/bitcoin-btc-closer-to-80000-than-60000-again-ethereums-eth-3000-recipe-hyperliquid-hype-bounce",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "BITSTAMP:ETHUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCETH"
          }
        ],
        "storyPath": "/news/u_today:9b36e2fa5094b:0-bitcoin-btc-closer-to-80-000-than-60-000-again-ethereum-s-eth-3-000-recipe-hyperliquid-hype-bounce-triggered-crypto-market-review/",
        "provider": {
          "id": "u_today",
          "name": "U.Today",
          "logo_id": "u-today",
          "url": "https://u.today"
        }
      },
      {
        "id": "newsbtc:52f8eafb1094b:0",
        "title": "Bitcoin And XRP Need Relief From Capital Drain, Says John Bollinger",
        "published": 1776895217,
        "urgency": 2,
        "link": "https://www.newsbtc.com/news/bitcoin-xrp-relief-capital-drain-john-bollinger/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "BITSTAMP:XRPUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCXRP"
          }
        ],
        "storyPath": "/news/newsbtc:52f8eafb1094b:0-bitcoin-and-xrp-need-relief-from-capital-drain-says-john-bollinger/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "u_today:2b249f276094b:0",
        "title": "Ripple Sends $108 Million XRP to Coinbase, Shiba Inu (SHIB) Sees April's Biggest Bullish Sign, Saylor’s Strategy Scoops $3.6 Billion Bitcoin Gains — U.Today Crypto Digest",
        "published": 1776894296,
        "urgency": 2,
        "link": "https://u.today/ripple-sends-108-million-xrp-to-coinbase-shiba-inu-shib-sees-aprils-biggest-bullish-sign-saylors",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:XRPUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCXRP"
          },
          {
            "symbol": "NASDAQ:MSTR",
            "logoid": "strategy-cad-hedged-cibc-cdr"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/u_today:2b249f276094b:0-ripple-sends-108-million-xrp-to-coinbase-shiba-inu-shib-sees-april-s-biggest-bullish-sign-saylor-s-strategy-scoops-3-6-billion-bitcoin-gains-u-today-crypto-digest/",
        "provider": {
          "id": "u_today",
          "name": "U.Today",
          "logo_id": "u-today",
          "url": "https://u.today"
        }
      },
      {
        "id": "u_today:278592f31094b:0",
        "title": "Ripple Sends $108 Million XRP to Coinbase, Shiba Inu (SHIB) Sees April's Biggest Bullish Sign,Saylor’s Strategy Scoops $3.6 Billion Bitcoin Gains — U.Today Crypto Digest",
        "published": 1776894296,
        "urgency": 2,
        "link": "https://u.today/ripple-sends-108-million-xrp-to-coinbase-shiba-inu-shib-sees-aprils-biggest-bullish-signsaylors",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:XRPUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCXRP"
          },
          {
            "symbol": "NASDAQ:MSTR",
            "logoid": "strategy-cad-hedged-cibc-cdr"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/u_today:278592f31094b:0-ripple-sends-108-million-xrp-to-coinbase-shiba-inu-shib-sees-april-s-biggest-bullish-sign-saylor-s-strategy-scoops-3-6-billion-bitcoin-gains-u-today-crypto-digest/",
        "provider": {
          "id": "u_today",
          "name": "U.Today",
          "logo_id": "u-today",
          "url": "https://u.today"
        }
      },
      {
        "id": "newsbtc:3c55261b0094b:0",
        "title": "$60,000 Is The Bottom: Bitcoin Analyst Predicts Lowest Level Before Run To $200,000",
        "published": 1776891611,
        "urgency": 2,
        "link": "https://www.newsbtc.com/news/bitcoin/60000-is-the-bitcoin-bottom/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:3c55261b0094b:0-60-000-is-the-bottom-bitcoin-analyst-predicts-lowest-level-before-run-to-200-000/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "forexlive:e6fceb537094b:0",
        "title": "Bitcoin rises as ETF inflows hit $1.5bn and short liquidations top $200m",
        "published": 1776890449,
        "urgency": 2,
        "link": "https://investinglive.com/Cryptocurrency/bitcoin-rises-as-etf-inflows-hit-15bn-and-short-liquidations-top-200m-20260422/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/forexlive:e6fceb537094b:0-bitcoin-rises-as-etf-inflows-hit-1-5bn-and-short-liquidations-top-200m/",
        "provider": {
          "id": "forexlive",
          "name": "InvestingLive",
          "logo_id": "forexlive",
          "url": "https://www.investinglive.com/"
        }
      },
      {
        "id": "u_today:32d31c160094b:0",
        "title": "Bitcoin Dominance Surpasses 60% First Time in 2026 as BTC Nears $80K",
        "published": 1776889909,
        "urgency": 2,
        "link": "https://u.today/bitcoin-dominance-surpasses-60-first-time-in-2026-as-btc-nears-80k",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/u_today:32d31c160094b:0-bitcoin-dominance-surpasses-60-first-time-in-2026-as-btc-nears-80k/",
        "provider": {
          "id": "u_today",
          "name": "U.Today",
          "logo_id": "u-today",
          "url": "https://u.today"
        }
      },
      {
        "id": "newsbtc:5eb202cae094b:0",
        "title": "Bears Are Fully In Control Of Bitcoin And It Will Crash Below $60,000, Here’s Why",
        "published": 1776888021,
        "urgency": 2,
        "link": "https://www.newsbtc.com/news/bitcoin/bears-in-control-bitcoin-60000/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:5eb202cae094b:0-bears-are-fully-in-control-of-bitcoin-and-it-will-crash-below-60-000-here-s-why/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "invezz:40d8f1691094b:0",
        "title": "Evening digest: Ukraine aid cleared, Iran Hormuz standoff deepens",
        "published": 1776887503,
        "urgency": 2,
        "link": "https://invezz.com/news/2026/04/22/evening-digest-ukraine-aid-cleared-iran-hormuz-standoff-deepens/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "TVC:UKOIL",
            "logoid": "crude-oil"
          }
        ],
        "storyPath": "/news/invezz:40d8f1691094b:0-evening-digest-ukraine-aid-cleared-iran-hormuz-standoff-deepens/",
        "provider": {
          "id": "invezz",
          "name": "Invezz",
          "logo_id": "invezz",
          "url": "https://invezz.com/"
        }
      },
      {
        "id": "bravenewcoin:a20740513094b:0",
        "title": "Bitcoin Breaks a Six-Month Pattern, Approaches $80,000",
        "published": 1776887328,
        "urgency": 2,
        "link": "https://bravenewcoin.com/insights/bitcoin-breaks-a-six-month-pattern-approaches-80000",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/bravenewcoin:a20740513094b:0/",
        "provider": {
          "id": "bravenewcoin",
          "name": "Brave New Coin",
          "logo_id": "bravenewcoin",
          "url": "https://bravenewcoin.com/"
        }
      },
      {
        "id": "beincrypto:5252c8ee4094b:0",
        "title": "US Military Runs Bitcoin Node for Cybersecurity Tests, Admiral Confirms",
        "published": 1776885935,
        "urgency": 2,
        "link": "https://beincrypto.com/us-military-bitcoin-node-indopacom/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/beincrypto:5252c8ee4094b:0-us-military-runs-bitcoin-node-for-cybersecurity-tests-admiral-confirms/",
        "provider": {
          "id": "beincrypto",
          "name": "Beincrypto",
          "logo_id": "beincrypto",
          "url": "https://beincrypto.com/"
        }
      },
      {
        "id": "DJN_DN20260422008422:0",
        "title": "Bitcoin Stability During War Underlies Longer-Term Shift — Market Talk",
        "published": 1776885780,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:ETHUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCETH"
          },
          {
            "symbol": "BINANCE:ETHUSDT",
            "currency-logoid": "crypto/XTVCUSDT",
            "base-currency-logoid": "crypto/XTVCETH"
          },
          {
            "symbol": "NYMEX:CL1!",
            "logoid": "crude-oil"
          },
          {
            "symbol": "TVC:USOIL",
            "logoid": "crude-oil"
          },
          {
            "symbol": "MCX:CRUDEOIL1!",
            "logoid": "crude-oil"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "BINANCE:BTCUSDT",
            "currency-logoid": "crypto/XTVCUSDT",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/DJN_DN20260422008422:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260422008322:0",
        "title": "Bitcoin Rides Tech Sector Gains. Is $100,000 Back in the Cards? — Barrons.com",
        "published": 1776884460,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/DJN_DN20260422008322:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "newsbtc:91f621508094b:0",
        "title": "Analyst Predicts Bitcoin Price Is Going To $200,000, Reveals When To Buy",
        "published": 1776880807,
        "urgency": 2,
        "link": "https://www.newsbtc.com/bitcoin-news/bitcoin-going-to-200000/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:91f621508094b:0-analyst-predicts-bitcoin-price-is-going-to-200-000-reveals-when-to-buy/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "cointelegraph:de8380127094b:0",
        "title": "Ethereum risks 10% decline versus Bitcoin despite record ETH staking",
        "published": 1776878347,
        "urgency": 2,
        "link": "https://cointelegraph.com/markets/ethereum-decline-10percent-versus-bitcoin-despite-record-eth-staking?utm_source=rss_feed&utm_medium=rss-trading-view_ETH&utm_campaign=rss_partner_inbound",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:ETHUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCETH"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/cointelegraph:de8380127094b:0-ethereum-risks-10-decline-versus-bitcoin-despite-record-eth-staking/",
        "provider": {
          "id": "cointelegraph",
          "name": "Cointelegraph",
          "logo_id": "cointelegraph-en",
          "url": "https://cointelegraph.com"
        }
      },
      {
        "id": "stocktwits:64ccbeef6094b:0",
        "title": "Bitcoin’s ‘Safe Haven’ Narrative Faces Real War Test While Iran Clock Ticks, Pompliano Doubles Down: Report",
        "published": 1776878199,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/cryptocurrency/bitcoins-safe-haven-narrative-faces-real-war-test/cZBBDQ2RebR",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/stocktwits:64ccbeef6094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_DN20260422007866:0",
        "title": "Bitcoin's Rally Is Just Getting Started. Technicals Speak to More Gains Ahead. — Barrons.com",
        "published": 1776877560,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/DJN_DN20260422007866:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "newsbtc:033df0523094b:0",
        "title": "$138M Bitcoin Play Triggers Rally, Signals Shift In Big Money Sentiment",
        "published": 1776877211,
        "urgency": 2,
        "link": "https://www.newsbtc.com/news/bitcoin/138m-bitcoin-play-triggers-rally-signals-shift-in-big-money-sentiment/",
        "relatedSymbols": [
          {
            "symbol": "NYSE:MS",
            "logoid": "morgan-stanley"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:033df0523094b:0-138m-bitcoin-play-triggers-rally-signals-shift-in-big-money-sentiment/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "DJN_DN20260422007677:0",
        "title": "Institutions See Bitcoin as Undervalued — Market Talk",
        "published": 1776875820,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/DJN_DN20260422007677:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260422007515:0",
        "title": "Bitcoin Nears $80,000 as Rebound Extends — Market Talk",
        "published": 1776874680,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/DJN_DN20260422007515:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "invezz:9a55514e4094b:0",
        "title": "MSTR stock leads crypto-linked rally as Bitcoin surges",
        "published": 1776873640,
        "urgency": 2,
        "link": "https://invezz.com/news/2026/04/22/mstr-stock-leads-crypto-linked-rally-as-bitcoin-surges/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSTR",
            "logoid": "strategy-cad-hedged-cibc-cdr"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/invezz:9a55514e4094b:0-mstr-stock-leads-crypto-linked-rally-as-bitcoin-surges/",
        "provider": {
          "id": "invezz",
          "name": "Invezz",
          "logo_id": "invezz",
          "url": "https://invezz.com/"
        }
      },
      {
        "id": "the_block:aedfde948094b:0",
        "title": "Eric Trump’s American Bitcoin rises 12% amid increase in BTC mining capacity",
        "published": 1776873605,
        "urgency": 2,
        "link": "https://www.theblock.co/post/398491/eric-trumps-american-bitcoin-rises-12-amid-increase-in-btc-mining-capacity?utm_source=tradingview&utm_medium=rss",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:ABTC",
            "logoid": "american-bitcoin"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/the_block:aedfde948094b:0-eric-trump-s-american-bitcoin-rises-12-amid-increase-in-btc-mining-capacity/",
        "provider": {
          "id": "the_block",
          "name": "The Block",
          "logo_id": "the-block",
          "url": "https://www.theblock.co/?utm_medium=rss&utm_source=tradingview"
        }
      },
      {
        "id": "invezz:07bf03236094b:0",
        "title": "Bitcoin up 10% as extended US–Iran ceasefire lifts market risk appetite",
        "published": 1776871958,
        "urgency": 2,
        "link": "https://invezz.com/news/2026/04/22/bitcoin-up-10-as-extended-us-iran-ceasefire-lifts-market-risk-appetite/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/invezz:07bf03236094b:0-bitcoin-up-10-as-extended-us-iran-ceasefire-lifts-market-risk-appetite/",
        "provider": {
          "id": "invezz",
          "name": "Invezz",
          "logo_id": "invezz",
          "url": "https://invezz.com/"
        }
      },
      {
        "id": "u_today:5a1572296094b:0",
        "title": "Bitcoin Hits $79,000 as a 4,362% Liquidation Imbalance Confirms a Massive Short Squeeze",
        "published": 1776871860,
        "urgency": 2,
        "link": "https://u.today/bitcoin-hits-79000-as-a-4362-liquidation-imbalance-confirms-a-massive-short-squeeze",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/u_today:5a1572296094b:0-bitcoin-hits-79-000-as-a-4-362-liquidation-imbalance-confirms-a-massive-short-squeeze/",
        "provider": {
          "id": "u_today",
          "name": "U.Today",
          "logo_id": "u-today",
          "url": "https://u.today"
        }
      },
      {
        "id": "u_today:55f9c3718094b:0",
        "title": "Anthony Pompliano Moves Satoshi Title to All Bitcoin Holders",
        "published": 1776871319,
        "urgency": 2,
        "link": "https://u.today/anthony-pompliano-moves-satoshi-title-to-all-bitcoin-holders",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/u_today:55f9c3718094b:0-anthony-pompliano-moves-satoshi-title-to-all-bitcoin-holders/",
        "provider": {
          "id": "u_today",
          "name": "U.Today",
          "logo_id": "u-today",
          "url": "https://u.today"
        }
      },
      {
        "id": "DJN_DN20260422006647:0",
        "title": "Bitcoin Behaving Like Hybrid Asset Amid Middle East Conflict — Market Talk",
        "published": 1776869640,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/DJN_DN20260422006647:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:0fde40b34094b:0",
        "title": "BlackRock Silently Scoops Nearly $1 Billion Of Bitcoin, Outpacing Weekly BTC Supply",
        "published": 1776868157,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/cryptocurrency/blackrock-silently-scoops-nearly-one-billion-of-bitcoin/cZBBrvuReGs",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NYSE:BLK",
            "logoid": "blackrock"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/stocktwits:0fde40b34094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_DN20260422006422:0",
        "title": "Documentary Claims to Solve $80 Billion Mystery at Heart of Bitcoin — WSJ",
        "published": 1776868080,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/DJN_DN20260422006422:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "forexlive:c8aa5418e094b:0",
        "title": "Bitcoin climbs to the highest since early February",
        "published": 1776867845,
        "urgency": 2,
        "link": "https://investinglive.com/Cryptocurrency/bitcoin-climbs-to-the-highest-since-early-february-20260422/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/forexlive:c8aa5418e094b:0-bitcoin-climbs-to-the-highest-since-early-february/",
        "provider": {
          "id": "forexlive",
          "name": "InvestingLive",
          "logo_id": "forexlive",
          "url": "https://www.investinglive.com/"
        }
      },
      {
        "id": "DJN_DN20260422006239:0",
        "title": "Crypto Turns Higher as Legislators Chew on the CLARITY Act — Market Talk",
        "published": 1776866640,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "BINANCE:BTCUSDT",
            "currency-logoid": "crypto/XTVCUSDT",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "BITSTAMP:ETHUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCETH"
          },
          {
            "symbol": "BINANCE:ETHUSDT",
            "currency-logoid": "crypto/XTVCUSDT",
            "base-currency-logoid": "crypto/XTVCETH"
          }
        ],
        "storyPath": "/news/DJN_DN20260422006239:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "newsbtc:70d267d26094b:0",
        "title": "Bitcoin Set For Stronger Week, Eyes $88K On Stable Macro Backdrop: Analyst",
        "published": 1776866409,
        "urgency": 2,
        "link": "https://www.newsbtc.com/news/bitcoin/bitcoin-set-for-stronger-week-eyes-88k-on-stable-macro-backdrop-analyst/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:70d267d26094b:0-bitcoin-set-for-stronger-week-eyes-88k-on-stable-macro-backdrop-analyst/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "the_block:29dc9acf6094b:0",
        "title": "Armed intruders force French family to transfer $820,000 in crypto: report",
        "published": 1776865539,
        "urgency": 2,
        "link": "https://www.theblock.co/post/398465/armed-intruders-force-french-family-to-transfer-820000-in-crypto-report?utm_source=tradingview&utm_medium=rss",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/the_block:29dc9acf6094b:0-armed-intruders-force-french-family-to-transfer-820-000-in-crypto-report/",
        "provider": {
          "id": "the_block",
          "name": "The Block",
          "logo_id": "the-block",
          "url": "https://www.theblock.co/?utm_medium=rss&utm_source=tradingview"
        }
      },
      {
        "id": "the_block:3797e9748094b:0",
        "title": "‘I suspect you got to the right answer’: New Satoshi documentary makes the case Hal Finney and Len Sassaman were Bitcoin’s co-creators",
        "published": 1776862862,
        "urgency": 2,
        "link": "https://www.theblock.co/post/398423/finding-satoshi-documentary-makes-case-hal-finney-len-sassaman-bitcoins-co-creators?utm_source=tradingview&utm_medium=rss",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/the_block:3797e9748094b:0-i-suspect-you-got-to-the-right-answer-new-satoshi-documentary-makes-the-case-hal-finney-and-len-sassaman-were-bitcoin-s-co-creators/",
        "provider": {
          "id": "the_block",
          "name": "The Block",
          "logo_id": "the-block",
          "url": "https://www.theblock.co/?utm_medium=rss&utm_source=tradingview"
        }
      },
      {
        "id": "newsbtc:3bd5d6fc8094b:0",
        "title": "Bitcoin Bull Score Index Turns Neutral For First Time This Bear Market",
        "published": 1776862817,
        "urgency": 2,
        "link": "https://www.newsbtc.com/bitcoin-news/bitcoin-bull-score-neutral-first-time-bear-market/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:3bd5d6fc8094b:0-bitcoin-bull-score-index-turns-neutral-for-first-time-this-bear-market/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "DJN_DN20260422005063:0",
        "title": "Stablecoins' Usage Could Reduce De-Dollarization Threat — Market Talk",
        "published": 1776860820,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/DJN_DN20260422005063:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260422004853:0",
        "title": "Bitcoin Has Scope to Recover Further — Market Talk",
        "published": 1776859740,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "BINANCE:BTCUSDT",
            "currency-logoid": "crypto/XTVCUSDT",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/DJN_DN20260422004853:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_SN20260422008641:0",
        "title": "Why Strategy's stock is outperforming bitcoin these days",
        "published": 1776859560,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSTR",
            "logoid": "strategy-cad-hedged-cibc-cdr"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/DJN_SN20260422008641:0/",
        "provider": {
          "id": "market-watch",
          "name": "MarketWatch",
          "logo_id": "marketwatch"
        }
      },
      {
        "id": "newsbtc:72092b3a6094b:0",
        "title": "Bitcoin Power Laws Predicts When Price Will Hit $1,000,000",
        "published": 1776859205,
        "urgency": 2,
        "link": "https://www.newsbtc.com/news/bitcoin/bitcoin-power-laws-1000000/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:72092b3a6094b:0-bitcoin-power-laws-predicts-when-price-will-hit-1-000-000/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "beincrypto:b9436eb9b094b:0",
        "title": "Russia Locks in July 1 Crypto Payments Regime to Bypass Sanctions",
        "published": 1776859159,
        "urgency": 2,
        "link": "https://beincrypto.com/russia-crypto-payments-foreign-trade-july/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/beincrypto:b9436eb9b094b:0-russia-locks-in-july-1-crypto-payments-regime-to-bypass-sanctions/",
        "provider": {
          "id": "beincrypto",
          "name": "Beincrypto",
          "logo_id": "beincrypto",
          "url": "https://beincrypto.com/"
        }
      },
      {
        "id": "cointelegraph:88a4ef87c094b:0",
        "title": "‘Powerful move’ looms for Bitcoin price, says Bollinger Bands indicator",
        "published": 1776857815,
        "urgency": 2,
        "link": "https://cointelegraph.com/news/powerful-move-looms-bitcoin-price-bollinger-bands-indicator?utm_source=rss_feed&utm_medium=rss-trading-view_BTC&utm_campaign=rss_partner_inbound",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/cointelegraph:88a4ef87c094b:0-powerful-move-looms-for-bitcoin-price-says-bollinger-bands-indicator/",
        "provider": {
          "id": "cointelegraph",
          "name": "Cointelegraph",
          "logo_id": "cointelegraph-en",
          "url": "https://cointelegraph.com"
        }
      },
      {
        "id": "chainwire:732d2d062094b:0",
        "title": "Bybit Launches Bybit Card Welcome Campaign Offering Up to 120 USDT in Rewards for New Users and First-Time Cardholders",
        "published": 1776856028,
        "urgency": 2,
        "link": "https://chainwire.org/2026/04/22/bybit-launches-bybit-card-welcome-campaign-offering-up-to-120-usdt-in-rewards-for-new-users-and-first-time-cardholders/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/chainwire:732d2d062094b:0-bybit-launches-bybit-card-welcome-campaign-offering-up-to-120-usdt-in-rewards-for-new-users-and-first-time-cardholders/",
        "provider": {
          "id": "chainwire",
          "name": "Chainwire",
          "logo_id": "chainwire",
          "url": "https://www.chainwire.org"
        }
      },
      {
        "id": "newsbtc:83c458822094b:0",
        "title": "Bitcoin Bottom At $63,000? Grayscale Research Flags Feb. 5 As This Cycle’s Low",
        "published": 1776855641,
        "urgency": 2,
        "link": "https://www.newsbtc.com/bitcoin-news/bitcoin-bottom-at-63000-grayscale-research-flags-feb-5-as-this-cycles-low/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:83c458822094b:0-bitcoin-bottom-at-63-000-grayscale-research-flags-feb-5-as-this-cycle-s-low/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "stocktwits:b706edebe094b:0",
        "title": "Bitcoin Tops $78,000 After Trump’s Ceasefire Extension – Analyst Sees ‘Heavier’ Breakouts For Altcoins",
        "published": 1776855374,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/cryptocurrency/bitcoin-tops-78-000-after-trump-s-ceasefire-extension-analyst-sees-heavier-breakouts-for-altcoins/cZBBVEEReGi",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/stocktwits:b706edebe094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "stocktwits:9290ea2e6094b:0",
        "title": "MSTR Stock Reportedly Draws Fresh $747M Bet From Capital Group Amid Bitcoin Rally",
        "published": 1776853518,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/mstr-stock-reportedly-draws-fresh-bet-from-capital-group-amid-bitcoin-rally/cZBBNX7ReGW",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSTR",
            "logoid": "strategy-cad-hedged-cibc-cdr"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/stocktwits:9290ea2e6094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "u_today:e9acaca45094b:0",
        "title": "Bitcoin Whales Stack $217 Million Bid Wall While Sell Zone Looms at $80,000",
        "published": 1776853284,
        "urgency": 2,
        "link": "https://u.today/bitcoin-whales-stack-217-million-bid-wall-while-sell-zone-looms-at-80000",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/u_today:e9acaca45094b:0-bitcoin-whales-stack-217-million-bid-wall-while-sell-zone-looms-at-80-000/",
        "provider": {
          "id": "u_today",
          "name": "U.Today",
          "logo_id": "u-today",
          "url": "https://u.today"
        }
      },
      {
        "id": "the_block:725bf3710094b:0",
        "title": "UK investors regain tax-free access to crypto ETNs via Innovative Finance ISA route",
        "published": 1776853097,
        "urgency": 2,
        "link": "https://www.theblock.co/post/398415/uk-investors-regain-tax-free-access-to-crypto-etns-via-innovative-finance-isa-route?utm_source=tradingview&utm_medium=rss",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "BITSTAMP:ETHUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCETH"
          }
        ],
        "storyPath": "/news/the_block:725bf3710094b:0-uk-investors-regain-tax-free-access-to-crypto-etns-via-innovative-finance-isa-route/",
        "provider": {
          "id": "the_block",
          "name": "The Block",
          "logo_id": "the-block",
          "url": "https://www.theblock.co/?utm_medium=rss&utm_source=tradingview"
        }
      },
      {
        "id": "u_today:3639c2260094b:0",
        "title": "BlackRock Spends $900 Million on Another Bitcoin Purchase",
        "published": 1776852935,
        "urgency": 2,
        "link": "https://u.today/blackrock-spends-900-million-on-another-bitcoin-purchase",
        "relatedSymbols": [
          {
            "symbol": "NYSE:BLK",
            "logoid": "blackrock"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/u_today:3639c2260094b:0-blackrock-spends-900-million-on-another-bitcoin-purchase/",
        "provider": {
          "id": "u_today",
          "name": "U.Today",
          "logo_id": "u-today",
          "url": "https://u.today"
        }
      },
      {
        "id": "cointelegraph:658f1a483094b:0",
        "title": "Bitcoin Bull Score hits six-month high as 2022 bear-market fears linger",
        "published": 1776852602,
        "urgency": 2,
        "link": "https://cointelegraph.com/news/bitcoin-bull-score-hits-six-month-high-2022-bear-market-fears-linger?utm_source=rss_feed&utm_medium=rss-trading-view&utm_campaign=rss_partner_inbound",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/cointelegraph:658f1a483094b:0-bitcoin-bull-score-hits-six-month-high-as-2022-bear-market-fears-linger/",
        "provider": {
          "id": "cointelegraph",
          "name": "Cointelegraph",
          "logo_id": "cointelegraph-en",
          "url": "https://cointelegraph.com"
        }
      },
      {
        "id": "invezz:1f3a0f28f094b:0",
        "title": "ADA eyes breakout as Bitcoin hits $78K and crypto rally gains pace",
        "published": 1776851633,
        "urgency": 2,
        "link": "https://invezz.com/news/2026/04/22/ada-eyes-breakout-as-bitcoin-hits-78k-and-crypto-rally-gains-pace/",
        "relatedSymbols": [
          {
            "symbol": "FX:ADAUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCADA"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "COINBASE:ADAUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCADA"
          }
        ],
        "storyPath": "/news/invezz:1f3a0f28f094b:0-ada-eyes-breakout-as-bitcoin-hits-78k-and-crypto-rally-gains-pace/",
        "provider": {
          "id": "invezz",
          "name": "Invezz",
          "logo_id": "invezz",
          "url": "https://invezz.com/"
        }
      },
      {
        "id": "beincrypto:226f6e6c7094b:0",
        "title": "MicroStrategy’s STRC Preferred Stock Buys 10X More Bitcoin Than All ETFs in 2026",
        "published": 1776850684,
        "urgency": 2,
        "link": "https://beincrypto.com/strategy-strc-bitcoin-purchases-outpace-etfs/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "CAPITALCOM:IBIT"
          },
          {
            "symbol": "NASDAQ:MSTR",
            "logoid": "strategy-cad-hedged-cibc-cdr"
          }
        ],
        "storyPath": "/news/beincrypto:226f6e6c7094b:0-microstrategy-s-strc-preferred-stock-buys-10x-more-bitcoin-than-all-etfs-in-2026/",
        "provider": {
          "id": "beincrypto",
          "name": "Beincrypto",
          "logo_id": "beincrypto",
          "url": "https://beincrypto.com/"
        }
      },
      {
        "id": "the_block:75a39d054094b:0",
        "title": "Bitcoin rises above $78,000, Fear & Greed Index exits ‘extreme fear’ zone",
        "published": 1776848978,
        "urgency": 2,
        "link": "https://www.theblock.co/post/398407/bitcoin-78000-escapes-extreme-fear?utm_source=tradingview&utm_medium=rss",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/the_block:75a39d054094b:0-bitcoin-rises-above-78-000-fear-greed-index-exits-extreme-fear-zone/",
        "provider": {
          "id": "the_block",
          "name": "The Block",
          "logo_id": "the-block",
          "url": "https://www.theblock.co/?utm_medium=rss&utm_source=tradingview"
        }
      },
      {
        "id": "coinpedia:d60ea5626094b:0",
        "title": "Bitcoin News: Why is Bitcoin Price up Today?",
        "published": 1776846747,
        "urgency": 2,
        "link": "https://coinpedia.org/news/bitcoin-news-why-is-bitcoin-price-up-today/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/coinpedia:d60ea5626094b:0-bitcoin-news-why-is-bitcoin-price-up-today/",
        "provider": {
          "id": "coinpedia",
          "name": "Coinpedia",
          "logo_id": "coinpedia",
          "url": "https://www.coinpedia.org/"
        }
      },
      {
        "id": "coinpedia:d740dff26094b:0",
        "title": "Exclusive: Arthur Hayes Sets $500K Bitcoin Target For End Of 2026, Backs HYPE At $200",
        "published": 1776846738,
        "urgency": 2,
        "link": "https://coinpedia.org/news/exclusive-arthur-hayes-sets-500k-bitcoin-target-for-end-of-2026-backs-hype-at-200/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/coinpedia:d740dff26094b:0-exclusive-arthur-hayes-sets-500k-bitcoin-target-for-end-of-2026-backs-hype-at-200/",
        "provider": {
          "id": "coinpedia",
          "name": "Coinpedia",
          "logo_id": "coinpedia",
          "url": "https://www.coinpedia.org/"
        }
      },
      {
        "id": "DJN_DN20260422001940:0",
        "title": "Bitcoin Price Surges Past $78,000 to 11-Week High. Why Cryptos Are Surging. — Barrons.com",
        "published": 1776846000,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/DJN_DN20260422001940:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "u_today:275218cd8094b:0",
        "title": "BItcoin's Qunatum Resistance is Here, But Charles Hoskinson Questions It: Explaining Why",
        "published": 1776845640,
        "urgency": 2,
        "link": "https://u.today/bitcoins-qunatum-resistance-is-here-but-charles-hoskinson-questions-it-explaining-why",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/u_today:275218cd8094b:0-bitcoin-s-qunatum-resistance-is-here-but-charles-hoskinson-questions-it-explaining-why/",
        "provider": {
          "id": "u_today",
          "name": "U.Today",
          "logo_id": "u-today",
          "url": "https://u.today"
        }
      },
      {
        "id": "DJN_SN20260422004213:0",
        "title": "Why these strategists say 45% of portfolios should be invested in gold, metals and bitcoin",
        "published": 1776843360,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "TASE:GOLD",
            "logoid": "gold"
          }
        ],
        "storyPath": "/news/DJN_SN20260422004213:0/",
        "provider": {
          "id": "market-watch",
          "name": "MarketWatch",
          "logo_id": "marketwatch"
        }
      },
      {
        "id": "tradingview:224e4b8af094b:0",
        "title": "BTC/USD: Bitcoin Tackles $78,000 in Upside Swing After Ceasefire Extension",
        "published": 1776842314,
        "urgency": 2,
        "link": "https://www.tradingview.com",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/tradingview:224e4b8af094b:0-btc-usd-bitcoin-tackles-78-000-in-upside-swing-after-ceasefire-extension/",
        "provider": {
          "id": "tradingview",
          "name": "TradingView",
          "logo_id": "tradingview-snaps"
        }
      },
      {
        "id": "DJN_DN20260422001643:0",
        "title": "Bitcoin Rises After Trump's Cease-Fire Extension Announcement — Market Talk",
        "published": 1776842100,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "BINANCE:BTCUSDT",
            "currency-logoid": "crypto/XTVCUSDT",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/DJN_DN20260422001643:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "beincrypto:b0a3f0ab5094b:0",
        "title": "Bitcoin Price Rally Masks a $35,000 On-Chain Gap Bulls Are Ignoring",
        "published": 1776839875,
        "urgency": 2,
        "link": "https://beincrypto.com/bitcoin-price-on-chain-gap-warning-analysis/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "CAPITALCOM:LTH",
            "logoid": "life-time-group"
          }
        ],
        "storyPath": "/news/beincrypto:b0a3f0ab5094b:0-bitcoin-price-rally-masks-a-35-000-on-chain-gap-bulls-are-ignoring/",
        "provider": {
          "id": "beincrypto",
          "name": "Beincrypto",
          "logo_id": "beincrypto",
          "url": "https://beincrypto.com/"
        }
      },
      {
        "id": "forexlive:7bbd6cfa1094b:0",
        "title": "Bitcoin price analysis today: Bulls press breakout zone as $78,250 the key line to watch",
        "published": 1776838808,
        "urgency": 2,
        "link": "https://investinglive.com/Cryptocurrency/bitcoin-price-analysis-today-bulls-press-breakout-zone-as-78250-the-key-line-to-watch-20260422/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/forexlive:7bbd6cfa1094b:0-bitcoin-price-analysis-today-bulls-press-breakout-zone-as-78-250-the-key-line-to-watch/",
        "provider": {
          "id": "forexlive",
          "name": "InvestingLive",
          "logo_id": "forexlive",
          "url": "https://www.investinglive.com/"
        }
      },
      {
        "id": "newsbtc:3c6f25524094b:0",
        "title": "Bitcoin’s Record Miner Sell-Off Casts Shadow Over Ceasefire-Fueled Rebound",
        "published": 1776837632,
        "urgency": 2,
        "link": "https://www.newsbtc.com/news/bitcoin/bitcoins-record-miner-sell-off-casts-shadow-over-ceasefire-fueled-rebound/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:3c6f25524094b:0-bitcoin-s-record-miner-sell-off-casts-shadow-over-ceasefire-fueled-rebound/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "u_today:6a06fc026094b:0",
        "title": "Brian Armstrong: New Satoshi Doc is the Best Yet",
        "published": 1776837059,
        "urgency": 2,
        "link": "https://u.today/brian-armstrong-new-satoshi-doc-is-the-best-yet",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/u_today:6a06fc026094b:0-brian-armstrong-new-satoshi-doc-is-the-best-yet/",
        "provider": {
          "id": "u_today",
          "name": "U.Today",
          "logo_id": "u-today",
          "url": "https://u.today"
        }
      },
      {
        "id": "beincrypto:6cf31596e094b:0",
        "title": "Grayscale Research Calls Bitcoin Bottom, Sees Early Bull Market Signals",
        "published": 1776835523,
        "urgency": 2,
        "link": "https://beincrypto.com/grayscale-bitcoin-bottom-65k-70k/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "NYSE:GRAY",
            "logoid": "grayscale"
          }
        ],
        "storyPath": "/news/beincrypto:6cf31596e094b:0-grayscale-research-calls-bitcoin-bottom-sees-early-bull-market-signals/",
        "provider": {
          "id": "beincrypto",
          "name": "Beincrypto",
          "logo_id": "beincrypto",
          "url": "https://beincrypto.com/"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L4N414162:0",
        "title": "Chinese crypto tycoon eyes Hong Kong capital with bitcoin asset management push",
        "published": 1776830723,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "HKEX:1611",
            "logoid": "sinohope-technology-ltd"
          },
          {
            "symbol": "NASDAQ:IBIT",
            "logoid": "ishares"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L4N414162:0-chinese-crypto-tycoon-eyes-hong-kong-capital-with-bitcoin-asset-management-push/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "newsbtc:c5ddda6b5094b:0",
        "title": "Bitcoin Price Rebound Accelerates, Traders Eye Strong Upside Continuation",
        "published": 1776824783,
        "urgency": 2,
        "link": "https://www.newsbtc.com/analysis/btc/bitcoin-price-rebound-76k/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:c5ddda6b5094b:0-bitcoin-price-rebound-accelerates-traders-eye-strong-upside-continuation/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "u_today:9a4bcb654094b:0",
        "title": "Does XRP Have a Chance? Unhealthy Bitcoin (BTC) Price Pattern Arises, Hyperliquid's (HYPE) $40 Will not Stay for Long: Crypto Market Review",
        "published": 1776816060,
        "urgency": 2,
        "link": "https://u.today/does-xrp-have-a-chance-unhealthy-bitcoin-btc-price-pattern-arises-hyperliquids-hype-40-will-not",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:XRPUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCXRP"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/u_today:9a4bcb654094b:0-does-xrp-have-a-chance-unhealthy-bitcoin-btc-price-pattern-arises-hyperliquid-s-hype-40-will-not-stay-for-long-crypto-market-review/",
        "provider": {
          "id": "u_today",
          "name": "U.Today",
          "logo_id": "u-today",
          "url": "https://u.today"
        }
      },
      {
        "id": "coinpedia:d1704a197094b:0",
        "title": "Coinbase Council: Preparing the Blockchain for the Quantum Era",
        "published": 1776813101,
        "urgency": 2,
        "link": "https://coinpedia.org/news/coinbase-council-preparing-the-blockchain-for-the-quantum-era/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:COIN",
            "logoid": "coinbase"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "BITSTAMP:ETHUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCETH"
          }
        ],
        "storyPath": "/news/coinpedia:d1704a197094b:0-coinbase-council-preparing-the-blockchain-for-the-quantum-era/",
        "provider": {
          "id": "coinpedia",
          "name": "Coinpedia",
          "logo_id": "coinpedia",
          "url": "https://www.coinpedia.org/"
        }
      },
      {
        "id": "newsbtc:8d2ac28d6094b:0",
        "title": "Anthony Scaramucci Puts Bitcoin Market Cap At $21 Trillion, So How Much Will 1 BTC Be?",
        "published": 1776807020,
        "urgency": 2,
        "link": "https://www.newsbtc.com/bitcoin-news/bitcoin-21-trillion-market-cap/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:8d2ac28d6094b:0-anthony-scaramucci-puts-bitcoin-market-cap-at-21-trillion-so-how-much-will-1-btc-be/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "beincrypto:0e6799866094b:0",
        "title": "Coinbase Publishes First Paper on Quantum Computing Position for Crypto",
        "published": 1776806003,
        "urgency": 2,
        "link": "https://beincrypto.com/coinbase-quantum-computing-blockchain-paper/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "BITSTAMP:ETHUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCETH"
          },
          {
            "symbol": "COINBASE:SOLUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCSOL"
          },
          {
            "symbol": "BITSTAMP:APTUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCAPTO"
          },
          {
            "symbol": "NASDAQ:COIN",
            "logoid": "coinbase"
          }
        ],
        "storyPath": "/news/beincrypto:0e6799866094b:0-coinbase-publishes-first-paper-on-quantum-computing-position-for-crypto/",
        "provider": {
          "id": "beincrypto",
          "name": "Beincrypto",
          "logo_id": "beincrypto",
          "url": "https://beincrypto.com/"
        }
      },
      {
        "id": "bravenewcoin:f1be5f67d094b:0",
        "title": "Bitcoin Clings to $75,000 as Warsh Cools Rate Bets and Strategy Eclipses BlackRock",
        "published": 1776805238,
        "urgency": 2,
        "link": "https://bravenewcoin.com/insights/bitcoin-clings-to-75000-as-warsh-cools-rate-bets-and-strategy-eclipses-blackrock",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "NASDAQ:MSTR",
            "logoid": "strategy-cad-hedged-cibc-cdr"
          }
        ],
        "storyPath": "/news/bravenewcoin:f1be5f67d094b:0/",
        "provider": {
          "id": "bravenewcoin",
          "name": "Brave New Coin",
          "logo_id": "bravenewcoin",
          "url": "https://bravenewcoin.com/"
        }
      },
      {
        "id": "invezz:360d7238a094b:0",
        "title": "Evening digest: Trump eyes Iran deal, Warsh pledges Fed independence",
        "published": 1776802320,
        "urgency": 2,
        "link": "https://invezz.com/news/2026/04/21/evening-digest-trump-iran-deal-hopes-warsh-pledges-fed-independence/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/invezz:360d7238a094b:0-evening-digest-trump-eyes-iran-deal-warsh-pledges-fed-independence/",
        "provider": {
          "id": "invezz",
          "name": "Invezz",
          "logo_id": "invezz",
          "url": "https://invezz.com/"
        }
      },
      {
        "id": "newsbtc:830a3d81b094b:0",
        "title": "Bitcoin Fear Fading? Sentiment Hits Highest Since Mid-January",
        "published": 1776796236,
        "urgency": 2,
        "link": "https://www.newsbtc.com/bitcoin-news/bitcoin-fear-fading-sentiment-highest-january/",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/newsbtc:830a3d81b094b:0-bitcoin-fear-fading-sentiment-hits-highest-since-mid-january/",
        "provider": {
          "id": "newsbtc",
          "name": "NewsBTC",
          "logo_id": "newsbtc",
          "url": "https://www.newsbtc.com"
        }
      },
      {
        "id": "cointelegraph:c18bf18ba094b:0",
        "title": "Bitcoin inflows to Binance fall to 2023 low as BTC bulls set target on $80K",
        "published": 1776794400,
        "urgency": 2,
        "link": "https://cointelegraph.com/news/bitcoin-inflows-to-binance-fall-to-2023-low-as-btc-bulls-set-target-on-dollar80k?utm_source=rss_feed&utm_medium=rss-trading-view_BTC&utm_campaign=rss_partner_inbound",
        "relatedSymbols": [
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          }
        ],
        "storyPath": "/news/cointelegraph:c18bf18ba094b:0-bitcoin-inflows-to-binance-fall-to-2023-low-as-btc-bulls-set-target-on-80k/",
        "provider": {
          "id": "cointelegraph",
          "name": "Cointelegraph",
          "logo_id": "cointelegraph-en",
          "url": "https://cointelegraph.com"
        }
      }
    ],
    "streaming": {
      "channel": "e988e978ac2ecd8bb735e98e1ff4"
    },
    "pagination": {
      "cursor": "eyJfaWQiOiJjb2ludGVsZWdyYXBoOmMxOGJmMThiYTA5NGIiLCJwdWJkYXRlIjoxNzc2Nzk0NDAwMDAwfQ=="
    }
  },
  "msg": "Success"
}
```

## Get Economic News

`GET /api/news/economic`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/api/news/economic?symbol=NASDAQ%3AAAPL&lang=en' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "invezz:59a983d12094b:0",
        "title": "What’s behind Apple’s strong iPhone growth in China market?",
        "published": 1776414277,
        "urgency": 2,
        "link": "https://invezz.com/news/2026/04/17/how-did-apple-boost-iphone-shipments-despite-china-market-slump/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/invezz:59a983d12094b:0-what-s-behind-apple-s-strong-iphone-growth-in-china-market/",
        "provider": {
          "id": "invezz",
          "name": "Invezz",
          "logo_id": "invezz",
          "url": "https://invezz.com/"
        }
      },
      {
        "id": "invezz:ebe27eb38094b:0",
        "title": "Apple cuts App Store fees in China to 25% amid antitrust pressure",
        "published": 1773385537,
        "urgency": 2,
        "link": "https://invezz.com/news/2026/03/13/apple-cuts-app-store-fees-in-china-as-regulatory-pressure-on-apple-tax-grows/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/invezz:ebe27eb38094b:0-apple-cuts-app-store-fees-in-china-to-25-amid-antitrust-pressure/",
        "provider": {
          "id": "invezz",
          "name": "Invezz",
          "logo_id": "invezz",
          "url": "https://invezz.com/"
        }
      },
      {
        "id": "invezz:62c8d69e5094b:0",
        "title": "Dow Jones Index futures today: eyes all-time high ahead of key catalysts",
        "published": 1769519760,
        "urgency": 2,
        "link": "https://invezz.com/news/2026/01/27/dow-jones-index-futures-today-eyes-all-time-high-ahead-of-key-catalysts/",
        "relatedSymbols": [
          {
            "symbol": "NYSE:UNH",
            "logoid": "unitedhealth"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:IBM",
            "logoid": "international-bus-mach"
          }
        ],
        "storyPath": "/news/invezz:62c8d69e5094b:0-dow-jones-index-futures-today-eyes-all-time-high-ahead-of-key-catalysts/",
        "provider": {
          "id": "invezz",
          "name": "Invezz",
          "logo_id": "invezz",
          "url": "https://invezz.com/"
        }
      },
      {
        "id": "invezz:995e5f5d7094b:0",
        "title": "Global markets brace for pivotal week as mega-cap tech earnings, Fed meet loom",
        "published": 1769254260,
        "urgency": 2,
        "link": "https://invezz.com/news/2026/01/24/global-markets-brace-for-pivotal-week-as-mega-cap-tech-earnings-fed-meet-loom/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          }
        ],
        "storyPath": "/news/invezz:995e5f5d7094b:0-global-markets-brace-for-pivotal-week-as-mega-cap-tech-earnings-fed-meet-loom/",
        "provider": {
          "id": "invezz",
          "name": "Invezz",
          "logo_id": "invezz",
          "url": "https://invezz.com/"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L1N3YA0CJ:0",
        "title": "US Commerce Secretary, New Delhi give differing accounts of breakdown in India trade talks",
        "published": 1767959374,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L1N3YA0CJ:0-us-commerce-secretary-new-delhi-give-differing-accounts-of-breakdown-in-india-trade-talks/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "invezz:5543f556e094b:0",
        "title": "A $10-trillion reckoning: how a Chinese invasion of Taiwan would upend markets",
        "published": 1767949200,
        "urgency": 2,
        "link": "https://invezz.com/news/2026/01/09/a-10-trillion-reckoning-how-a-chinese-invasion-of-taiwan-would-upend-world-markets/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "TWSE:2330",
            "logoid": "taiwan-semiconductor"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/invezz:5543f556e094b:0-a-10-trillion-reckoning-how-a-chinese-invasion-of-taiwan-would-upend-markets/",
        "provider": {
          "id": "invezz",
          "name": "Invezz",
          "logo_id": "invezz",
          "url": "https://invezz.com/"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L1N3YA059:0",
        "title": "India-US trade deal stalled after Modi did not call Trump, Lutnick says",
        "published": 1767938535,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L1N3YA059:0-india-us-trade-deal-stalled-after-modi-did-not-call-trump-lutnick-says/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "invezz:c549c529e094b:0",
        "title": "India clears $4.6B electronics component push as firms diversify from China",
        "published": 1767360789,
        "urgency": 2,
        "link": "https://invezz.com/news/2026/01/02/india-clears-4-6b-electronics-component-push-as-firms-diversify-from-china/",
        "relatedSymbols": [
          {
            "symbol": "KRX:005930",
            "logoid": "samsung"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/invezz:c549c529e094b:0-india-clears-4-6b-electronics-component-push-as-firms-diversify-from-china/",
        "provider": {
          "id": "invezz",
          "name": "Invezz",
          "logo_id": "invezz",
          "url": "https://invezz.com/"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L1N3XF07U:0",
        "title": "AI demand powers Taiwan November exports to fastest growth in 15-1/2 years",
        "published": 1765270143,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "TWSE:2330",
            "logoid": "taiwan-semiconductor"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L1N3XF07U:0-ai-demand-powers-taiwan-november-exports-to-fastest-growth-in-15-1-2-years/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "invezz:38a57ce11094b:0",
        "title": "Morning Brief: Disney’s CEO search intensifies; Apple’s AI chief steps down",
        "published": 1764655385,
        "urgency": 2,
        "link": "https://invezz.com/news/2025/12/02/morning-brief-disneys-ceo-search-intensifies-apples-ai-chief-steps-down/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "NYSE:DIS",
            "logoid": "walt-disney"
          }
        ],
        "storyPath": "/news/invezz:38a57ce11094b:0-morning-brief-disney-s-ceo-search-intensifies-apple-s-ai-chief-steps-down/",
        "provider": {
          "id": "invezz",
          "name": "Invezz",
          "logo_id": "invezz",
          "url": "https://invezz.com/"
        }
      },
      {
        "id": "invezz:10963bcae094b:0",
        "title": "Evening digest: Intel soars on Apple hopes, China pressures the UK, India’s growth beats forecasts",
        "published": 1764358779,
        "urgency": 2,
        "link": "https://invezz.com/news/2025/11/28/evening-digest-intel-soars-on-apple-hopes-china-pressures-the-uk-indias-growth-beats-forecasts/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:INTC",
            "logoid": "intel"
          },
          {
            "symbol": "OMXSTO:CS"
          }
        ],
        "storyPath": "/news/invezz:10963bcae094b:0-evening-digest-intel-soars-on-apple-hopes-china-pressures-the-uk-india-s-growth-beats-forecasts/",
        "provider": {
          "id": "invezz",
          "name": "Invezz",
          "logo_id": "invezz",
          "url": "https://invezz.com/"
        }
      },
      {
        "id": "invezz:a9e342dfa094b:0",
        "title": "America’s trillion dollar promise: Is the “Trump Effect” real?",
        "published": 1764241200,
        "urgency": 2,
        "link": "https://invezz.com/news/2025/11/27/americas-trillion-dollar-promise-is-the-trump-effect-real/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "TSE:9984",
            "logoid": "softbank"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "TWSE:2330",
            "logoid": "taiwan-semiconductor"
          },
          {
            "symbol": "NYSE:ORCL",
            "logoid": "oracle"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          }
        ],
        "storyPath": "/news/invezz:a9e342dfa094b:0-america-s-trillion-dollar-promise-is-the-trump-effect-real/",
        "provider": {
          "id": "invezz",
          "name": "Invezz",
          "logo_id": "invezz",
          "url": "https://invezz.com/"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L6N3WM0HA:0",
        "title": "Trump's trade war with China in 2025",
        "published": 1762853538,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:QCOM",
            "logoid": "qualcomm"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L6N3WM0HA:0-trump-s-trade-war-with-china-in-2025/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "invezz:71723dd95094b:0",
        "title": "Weekly wrap: Mamdani win, SC questions Trump’s tariffs, Tesla approves Musk pay package",
        "published": 1762617840,
        "urgency": 2,
        "link": "https://invezz.com/news/2025/11/08/weekly-wrap-mamdani-win-sc-questions-trumps-tariffs-tesla-approves-musk-pay-package/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          }
        ],
        "storyPath": "/news/invezz:71723dd95094b:0-weekly-wrap-mamdani-win-sc-questions-trump-s-tariffs-tesla-approves-musk-pay-package/",
        "provider": {
          "id": "invezz",
          "name": "Invezz",
          "logo_id": "invezz",
          "url": "https://invezz.com/"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L1N3WJ09V:0",
        "title": "Taiwan October exports log biggest growth in nearly 16 years on strong AI demand",
        "published": 1762506336,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "TWSE:2330",
            "logoid": "taiwan-semiconductor"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L1N3WJ09V:0-taiwan-october-exports-log-biggest-growth-in-nearly-16-years-on-strong-ai-demand/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "invezz:be5e58717094b:0",
        "title": "Big tech surges to all time highs as AI costs outweigh human costs",
        "published": 1761892819,
        "urgency": 2,
        "link": "https://invezz.com/news/2025/10/31/big-tech-surges-to-all-time-highs-as-ai-costs-outweigh-human-costs/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          }
        ],
        "storyPath": "/news/invezz:be5e58717094b:0-big-tech-surges-to-all-time-highs-as-ai-costs-outweigh-human-costs/",
        "provider": {
          "id": "invezz",
          "name": "Invezz",
          "logo_id": "invezz",
          "url": "https://invezz.com/"
        }
      },
      {
        "id": "invezz:a22aa454a094b:0",
        "title": "Dow futures soar over 260 points on US-China deal: 5 things to know before Wall Street opens",
        "published": 1761563967,
        "urgency": 2,
        "link": "https://invezz.com/news/2025/10/27/dow-futures-soar-over-260-points-on-us-china-deal-5-things-to-know-before-wall-street-opens/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          }
        ],
        "storyPath": "/news/invezz:a22aa454a094b:0-dow-futures-soar-over-260-points-on-us-china-deal-5-things-to-know-before-wall-street-opens/",
        "provider": {
          "id": "invezz",
          "name": "Invezz",
          "logo_id": "invezz",
          "url": "https://invezz.com/"
        }
      },
      {
        "id": "invezz:92e3f971e094b:0",
        "title": "Interview: ‘underperformance is punished more than outperformance is rewarded’ says analyst Joshua Mahony on Wall Street outlook",
        "published": 1760956535,
        "urgency": 2,
        "link": "https://invezz.com/news/2025/10/20/interview-underperformance-is-punished-more-than-outperformance-is-rewarded-says-analyst-joshua-mahony-on-wall-street-outlook/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/invezz:92e3f971e094b:0-interview-underperformance-is-punished-more-than-outperformance-is-rewarded-says-analyst-joshua-mahony-on-wall-street-outlook/",
        "provider": {
          "id": "invezz",
          "name": "Invezz",
          "logo_id": "invezz",
          "url": "https://invezz.com/"
        }
      },
      {
        "id": "invezz:1958ddd24094b:0",
        "title": "Morning brief: ‘No Kings’ protest, Heist at the Louvre, Bolivia elects new leader",
        "published": 1760933598,
        "urgency": 2,
        "link": "https://invezz.com/news/2025/10/20/morning-brief-no-kings-protest-heist-at-the-louvre-bolivia-elects-new-leader/",
        "relatedSymbols": [
          {
            "symbol": "NYSE:TWTR",
            "logoid": "twitter"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          }
        ],
        "storyPath": "/news/invezz:1958ddd24094b:0-morning-brief-no-kings-protest-heist-at-the-louvre-bolivia-elects-new-leader/",
        "provider": {
          "id": "invezz",
          "name": "Invezz",
          "logo_id": "invezz",
          "url": "https://invezz.com/"
        }
      },
      {
        "id": "invezz:984688d4c094b:0",
        "title": "Morning brief: US-China tensions; a Russian LNG test; new Trump tariffs",
        "published": 1760416794,
        "urgency": 2,
        "link": "https://invezz.com/news/2025/10/14/morning-brief-us-china-tensions-a-russian-lng-test-new-trump-tariffs/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "EURONEXT:ASML",
            "logoid": "asml"
          },
          {
            "symbol": "XETR:SAP",
            "logoid": "sap"
          },
          {
            "symbol": "HKEX:9992",
            "logoid": "pop-mart-intl-grp-ltd"
          }
        ],
        "storyPath": "/news/invezz:984688d4c094b:0-morning-brief-us-china-tensions-a-russian-lng-test-new-trump-tariffs/",
        "provider": {
          "id": "invezz",
          "name": "Invezz",
          "logo_id": "invezz",
          "url": "https://invezz.com/"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L2N3VQ09I:0",
        "title": "Taiwan Sept exports misses forecasts, AI demand remains strong",
        "published": 1760000437,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "TWSE:2330",
            "logoid": "taiwan-semiconductor"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L2N3VQ09I:0-taiwan-sept-exports-misses-forecasts-ai-demand-remains-strong/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "invezz:4ef67d18d094b:0",
        "title": "Europe bulletin: markets rise, Starmer’s India visit, Germany’s Temu probe",
        "published": 1759944776,
        "urgency": 2,
        "link": "https://invezz.com/news/2025/10/08/europe-bulletin-markets-rise-starmers-india-visit-germanys-temu-probe/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "TVC:UKX",
            "logoid": "indices/uk-100"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "EURONEXT:PX1",
            "logoid": "indices/cac-40"
          }
        ],
        "storyPath": "/news/invezz:4ef67d18d094b:0-europe-bulletin-markets-rise-starmer-s-india-visit-germany-s-temu-probe/",
        "provider": {
          "id": "invezz",
          "name": "Invezz",
          "logo_id": "invezz",
          "url": "https://invezz.com/"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L6N3UW0TA:0",
        "title": "Apple holds down new iPhone prices amid threats of Trump tariffs",
        "published": 1757434804,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "KRX:005930",
            "logoid": "samsung"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AVGO",
            "logoid": "broadcom"
          },
          {
            "symbol": "NASDAQ:QCOM",
            "logoid": "qualcomm"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L6N3UW0TA:0-apple-holds-down-new-iphone-prices-amid-threats-of-trump-tariffs/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "invezz:b6e57c8ad094b:0",
        "title": "US stocks open flat ahead of inflation data: S&P, Nasdaq up 0.2%",
        "published": 1757425845,
        "urgency": 2,
        "link": "https://invezz.com/news/2025/09/09/us-stocks-open-flat-ahead-of-inflation-data-sp-nasdaq-up-0-2/",
        "relatedSymbols": [
          {
            "symbol": "TVC:DJI",
            "logoid": "indices/dow-30"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/invezz:b6e57c8ad094b:0-us-stocks-open-flat-ahead-of-inflation-data-s-p-nasdaq-up-0-2/",
        "provider": {
          "id": "invezz",
          "name": "Invezz",
          "logo_id": "invezz",
          "url": "https://invezz.com/"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L2N3UW08H:0",
        "title": "Taiwan August exports beats forecasts to hit record level despite tariffs",
        "published": 1757408220,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "TWSE:2330",
            "logoid": "taiwan-semiconductor"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L2N3UW08H:0-taiwan-august-exports-beats-forecasts-to-hit-record-level-despite-tariffs/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L8N3UD0IO:0",
        "title": "Major developments in Trump's trade war",
        "published": 1755775054,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L8N3UD0IO:0-major-developments-in-trump-s-trade-war/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L6N3UC0S9:0",
        "title": "Masimo sues US Customs over approval of Apple Watch imports",
        "published": 1755729822,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MASI",
            "logoid": "masimo"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L6N3UC0S9:0-masimo-sues-us-customs-over-approval-of-apple-watch-imports/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L1N3U70DV:0",
        "title": "Trump says he will set tariffs on steel and semiconductor chips in coming weeks",
        "published": 1755264200,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L1N3U70DV:0-trump-says-he-will-set-tariffs-on-steel-and-semiconductor-chips-in-coming-weeks/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L4N3U70CD:0",
        "title": "Global equity fund inflows at six-week high on soft US inflation, tariff truce",
        "published": 1755250515,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L4N3U70CD:0-global-equity-fund-inflows-at-six-week-high-on-soft-us-inflation-tariff-truce/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L4N3U309E:0",
        "title": "In India, Trump's tariffs spark calls to boycott American goods",
        "published": 1754898604,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NSE:TCS",
            "logoid": "tata"
          },
          {
            "symbol": "NSE:INFY1!",
            "logoid": "infosys"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NYSE:MCD",
            "logoid": "mcdonalds"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:KO",
            "logoid": "coca-cola"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L4N3U309E:0-in-india-trump-s-tariffs-spark-calls-to-boycott-american-goods/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L6N3TZ15G:0",
        "title": "Intel fabricates a hopeless trade war predicament",
        "published": 1754654400,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:INTC",
            "logoid": "intel"
          },
          {
            "symbol": "TWSE:2330",
            "logoid": "taiwan-semiconductor"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NYSE:GM",
            "logoid": "general-motors"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L6N3TZ15G:0-intel-fabricates-a-hopeless-trade-war-predicament/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L1N3U00E3:0",
        "title": "Taiwan July exports post fastest growth in 15 years on strong tech demand",
        "published": 1754643474,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "TWSE:2330",
            "logoid": "taiwan-semiconductor"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L1N3U00E3:0-taiwan-july-exports-post-fastest-growth-in-15-years-on-strong-tech-demand/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L6N3TZ0EK:0",
        "title": "Trump's chip tariff exemptions offer false comfort",
        "published": 1754568003,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "TWSE:2330",
            "logoid": "taiwan-semiconductor"
          },
          {
            "symbol": "KRX:005930",
            "logoid": "samsung"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L6N3TZ0EK:0-trump-s-chip-tariff-exemptions-offer-false-comfort/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L8N3TZ0JT:0",
        "title": "Apple shares rise as US investment pledge eases tariff concerns",
        "published": 1754547366,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L8N3TZ0JT:0-apple-shares-rise-as-us-investment-pledge-eases-tariff-concerns/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L4N3TR1R2:0",
        "title": "Apple earnings under pressure from tariffs, slow AI roll-out",
        "published": 1753887898,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L4N3TR1R2:0-apple-earnings-under-pressure-from-tariffs-slow-ai-roll-out/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L8N3TB0EZ:0",
        "title": "Trump's trade war as it unfolds",
        "published": 1752484100,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NYSE:GM",
            "logoid": "general-motors"
          },
          {
            "symbol": "NYSE:F",
            "logoid": "ford"
          },
          {
            "symbol": "MIL:STLAM",
            "logoid": "stellantis"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L8N3TB0EZ:0-trump-s-trade-war-as-it-unfolds/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L1N3T506P:0",
        "title": "Taiwan's exports in June beat forecasts to hit a record again",
        "published": 1751965355,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "TWSE:2330",
            "logoid": "taiwan-semiconductor"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L1N3T506P:0-taiwan-s-exports-in-june-beat-forecasts-to-hit-a-record-again/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L4N3T10BO:0",
        "title": "Big tech rules, agriculture among issues in US trade talks with South Korea",
        "published": 1751860603,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NYSE:BABA",
            "logoid": "alibaba"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "KRX:035420",
            "logoid": "naver"
          },
          {
            "symbol": "KRX:035720",
            "logoid": "kakao"
          },
          {
            "symbol": "NASDAQ:NFLX",
            "logoid": "netflix"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L4N3T10BO:0-big-tech-rules-agriculture-among-issues-in-us-trade-talks-with-south-korea/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L4N3SX0OM:0",
        "title": "Tech stocks up as Canada scraps digital services tax to advance US trade talks",
        "published": 1751279652,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L4N3SX0OM:0-tech-stocks-up-as-canada-scraps-digital-services-tax-to-advance-us-trade-talks/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L1N3SG05N:0",
        "title": "Foxconn sends 97% of India iPhone exports to US as Apple tackles Trump's tariffs",
        "published": 1749791619,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "TWSE:2354",
            "logoid": "foxconn-tech-co"
          }
        ],
        "isExclusive": true,
        "storyPath": "/news/reuters.com,2025:newsml_L1N3SG05N:0-foxconn-sends-97-of-india-iphone-exports-to-us-as-apple-tackles-trump-s-tariffs/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L6N3SC0OS:0",
        "title": "S&P 500 ends slightly up; traders watch US-China trade talks",
        "published": 1749500449,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "SP:S5UTIL",
            "logoid": "sector/utilities"
          },
          {
            "symbol": "SP:SPF",
            "logoid": "sector/financial"
          },
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "NASDAQ:WBD",
            "logoid": "warner-bros-discovery"
          },
          {
            "symbol": "NASDAQ:HOOD",
            "logoid": "robinhood"
          },
          {
            "symbol": "TVC:DJI",
            "logoid": "indices/dow-30"
          },
          {
            "symbol": "NASDAQ:NDAQ",
            "logoid": "nasdaq"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L6N3SC0OS:0-s-p-500-ends-slightly-up-traders-watch-us-china-trade-talks/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L1N3SC06Z:0",
        "title": "Taiwan May exports hit record on AI demand and ahead of US tariffs",
        "published": 1749459598,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "TWSE:2330",
            "logoid": "taiwan-semiconductor"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L1N3SC06Z:0-taiwan-may-exports-hit-record-on-ai-demand-and-ahead-of-us-tariffs/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L3N3S905L:0",
        "title": "Vietnam's trade surplus with US surges, complicating tariff talks",
        "published": 1749178569,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:INTC",
            "logoid": "intel"
          },
          {
            "symbol": "NYSE:NKE",
            "logoid": "nike"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L3N3S905L:0-vietnam-s-trade-surplus-with-us-surges-complicating-tariff-talks/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L3N3S715I:0",
        "title": "Apple and Alibaba's AI rollout in China delayed by Trump's trade war, FT reports",
        "published": 1749052881,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:BABA",
            "logoid": "alibaba"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L3N3S715I:0-apple-and-alibaba-s-ai-rollout-in-china-delayed-by-trump-s-trade-war-ft-reports/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L3N3S70DA:0",
        "title": "Counterpoint Research cuts 2025 global smartphone shipment growth amid tariff uncertainty",
        "published": 1749022342,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "KRX:005930",
            "logoid": "samsung"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L3N3S70DA:0-counterpoint-research-cuts-2025-global-smartphone-shipment-growth-amid-tariff-uncertainty/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L5N3S604N:0",
        "title": "US made 'tough' requests to Vietnam in trade talks, sources say",
        "published": 1748943892,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NYSE:NKE",
            "logoid": "nike"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "isExclusive": true,
        "storyPath": "/news/reuters.com,2025:newsml_L5N3S604N:0-us-made-tough-requests-to-vietnam-in-trade-talks-sources-say/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L2N3S505K:0",
        "title": "How Trump's trade war is upending the global economy",
        "published": 1748845714,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NYSE:GM",
            "logoid": "general-motors"
          },
          {
            "symbol": "NYSE:F",
            "logoid": "ford"
          },
          {
            "symbol": "MIL:STLAM",
            "logoid": "stellantis"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L2N3S505K:0-how-trump-s-trade-war-is-upending-the-global-economy/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L2N3S2074:0",
        "title": "China, HK shares drop on US tariff concerns, auto makers tumble",
        "published": 1748595485,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "SZSE:399300"
          },
          {
            "symbol": "SSE:000001",
            "logoid": "indices/sse-composite"
          },
          {
            "symbol": "HSI:HSCEI",
            "logoid": "indices/hang-seng-china-enterprises"
          },
          {
            "symbol": "HSI:HSI",
            "logoid": "indices/hang-seng"
          },
          {
            "symbol": "SSE:601138",
            "logoid": "foxconn-industrial-internet"
          },
          {
            "symbol": "HKEX:285",
            "logoid": "byd-electronic"
          },
          {
            "symbol": "SZSE:300433",
            "logoid": "lens-technology-co"
          },
          {
            "symbol": "HKEX:9868",
            "logoid": "xpeng"
          },
          {
            "symbol": "SZSE:002594",
            "logoid": "byd-electronic"
          },
          {
            "symbol": "NYSE:NIO",
            "logoid": "nio"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "TWSE:2354",
            "logoid": "foxconn-tech-co"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L2N3S2074:0-china-hk-shares-drop-on-us-tariff-concerns-auto-makers-tumble/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L2N3S205A:0",
        "title": "China, HK-listed Apple suppliers fall as US court reinstates Trump tariffs",
        "published": 1748587568,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "SZSE:002475",
            "logoid": "luxshare-precision"
          },
          {
            "symbol": "SZSE:300433",
            "logoid": "lens-technology-co"
          },
          {
            "symbol": "SZSE:002241",
            "logoid": "goertek-inc"
          },
          {
            "symbol": "SZSE:399300"
          },
          {
            "symbol": "SSE:000001",
            "logoid": "indices/sse-composite"
          },
          {
            "symbol": "HKEX:1415",
            "logoid": "cowell-e"
          },
          {
            "symbol": "HKEX:2018",
            "logoid": "aac-tech"
          },
          {
            "symbol": "HKEX:2382",
            "logoid": "sunny-optical"
          },
          {
            "symbol": "HKEX:285",
            "logoid": "byd-electronic"
          },
          {
            "symbol": "HSI:HSTECH"
          },
          {
            "symbol": "HSI:HSI",
            "logoid": "indices/hang-seng"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L2N3S205A:0-china-hk-listed-apple-suppliers-fall-as-us-court-reinstates-trump-tariffs/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L2N3S203H:0",
        "title": "China, HK shares dip as Apple suppliers slip on tariff concerns, auto makers tumble",
        "published": 1748580570,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "SZSE:399300"
          },
          {
            "symbol": "SSE:000001",
            "logoid": "indices/sse-composite"
          },
          {
            "symbol": "HSI:HSCEI",
            "logoid": "indices/hang-seng-china-enterprises"
          },
          {
            "symbol": "SSE:601138",
            "logoid": "foxconn-industrial-internet"
          },
          {
            "symbol": "HKEX:285",
            "logoid": "byd-electronic"
          },
          {
            "symbol": "SZSE:300433",
            "logoid": "lens-technology-co"
          },
          {
            "symbol": "HKEX:9868",
            "logoid": "xpeng"
          },
          {
            "symbol": "SZSE:002594",
            "logoid": "byd-electronic"
          },
          {
            "symbol": "NYSE:NIO",
            "logoid": "nio"
          },
          {
            "symbol": "TVC:NI225",
            "logoid": "indices/nikkei-225"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "TWSE:2354",
            "logoid": "foxconn-tech-co"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L2N3S203H:0-china-hk-shares-dip-as-apple-suppliers-slip-on-tariff-concerns-auto-makers-tumble/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L2N3S1055:0",
        "title": "China-listed Apple Suppliers rise after US court blocks most Trump tariffs",
        "published": 1748496478,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "SZSE:300433",
            "logoid": "lens-technology-co"
          },
          {
            "symbol": "SZSE:002241",
            "logoid": "goertek-inc"
          },
          {
            "symbol": "HKEX:1415",
            "logoid": "cowell-e"
          },
          {
            "symbol": "HKEX:2018",
            "logoid": "aac-tech"
          },
          {
            "symbol": "HKEX:2382",
            "logoid": "sunny-optical"
          },
          {
            "symbol": "HKEX:285",
            "logoid": "byd-electronic"
          },
          {
            "symbol": "HSI:HSTECH"
          },
          {
            "symbol": "HSI:HSI",
            "logoid": "indices/hang-seng"
          },
          {
            "symbol": "SZSE:399300"
          },
          {
            "symbol": "SSE:000001",
            "logoid": "indices/sse-composite"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L2N3S1055:0-china-listed-apple-suppliers-rise-after-us-court-blocks-most-trump-tariffs/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L3N3RZ10U:0",
        "title": "Wall St rises more than 1% as Trump backs down on EU tariffs",
        "published": 1748361257,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "DJ:DJI",
            "logoid": "indices/dow-30"
          },
          {
            "symbol": "SP:SPX",
            "logoid": "indices/s-and-p-500"
          },
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "SP:S5COND",
            "logoid": "sector/consumer-discretionary"
          },
          {
            "symbol": "SP:S5INFT",
            "logoid": "sector/information-technology"
          },
          {
            "symbol": "NASDAQ:PDD",
            "logoid": "pinduoduo"
          },
          {
            "symbol": "TVC:DJI",
            "logoid": "indices/dow-30"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L3N3RZ10U:0-wall-st-rises-more-than-1-as-trump-backs-down-on-eu-tariffs/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L3N3RZ0VZ:0",
        "title": "Wall St climbs after long weekend on Trump's EU tariff reprieve",
        "published": 1748355850,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "DJ:DJI",
            "logoid": "indices/dow-30"
          },
          {
            "symbol": "SP:SPX",
            "logoid": "indices/s-and-p-500"
          },
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "SP:S5COND",
            "logoid": "sector/consumer-discretionary"
          },
          {
            "symbol": "SP:S5INFT",
            "logoid": "sector/information-technology"
          },
          {
            "symbol": "NASDAQ:PDD",
            "logoid": "pinduoduo"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L3N3RZ0VZ:0-wall-st-climbs-after-long-weekend-on-trump-s-eu-tariff-reprieve/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L3N3RZ0FJ:0",
        "title": "US trade war tangles tanks and t-shirts",
        "published": 1748347200,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "HKEX:80992",
            "logoid": "lenovo"
          },
          {
            "symbol": "HKEX:551",
            "logoid": "yue-yuen-industrial"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "SZSE:002241",
            "logoid": "goertek-inc"
          },
          {
            "symbol": "SZSE:002475",
            "logoid": "luxshare-precision"
          },
          {
            "symbol": "HKEX:992",
            "logoid": "lenovo"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L3N3RZ0FJ:0-us-trade-war-tangles-tanks-and-t-shirts/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L3N3RZ0LJ:0",
        "title": "US stock futures rally after long weekend on Trump's tariff reprieve",
        "published": 1748345298,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "CME_MINI:ES1!",
            "logoid": "indices/s-and-p-500"
          },
          {
            "symbol": "CME_MINI:NQ1!",
            "logoid": "indices/nasdaq-100"
          },
          {
            "symbol": "NASDAQ:DJT",
            "logoid": "digital-world-acquisition-corp"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "SP:SPX",
            "logoid": "indices/s-and-p-500"
          },
          {
            "symbol": "NASDAQ:PDD",
            "logoid": "pinduoduo"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L3N3RZ0LJ:0-us-stock-futures-rally-after-long-weekend-on-trump-s-tariff-reprieve/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L5N3RY03O:0",
        "title": "How Trump's trade war is upending global economy",
        "published": 1748238337,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NYSE:GM",
            "logoid": "general-motors"
          },
          {
            "symbol": "NYSE:F",
            "logoid": "ford"
          },
          {
            "symbol": "MIL:STLAM",
            "logoid": "stellantis"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L5N3RY03O:0-how-trump-s-trade-war-is-upending-global-economy/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L2N3RY01J:0",
        "title": "Cowell leads slide in HK-listed Apple suppliers on Trump's tariff threat",
        "published": 1748228114,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "HKEX:1415",
            "logoid": "cowell-e"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "HKEX:2018",
            "logoid": "aac-tech"
          },
          {
            "symbol": "SZSE:300433",
            "logoid": "lens-technology-co"
          },
          {
            "symbol": "SZSE:002241",
            "logoid": "goertek-inc"
          },
          {
            "symbol": "HSI:HSTECH"
          },
          {
            "symbol": "HSI:HSI",
            "logoid": "indices/hang-seng"
          },
          {
            "symbol": "SZSE:399300"
          },
          {
            "symbol": "SSE:000001",
            "logoid": "indices/sse-composite"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L2N3RY01J:0-cowell-leads-slide-in-hk-listed-apple-suppliers-on-trump-s-tariff-threat/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L2N3RY01A:0",
        "title": "South Korean shares rise 1% as Trump delays EU tariffs, battery makers rebound",
        "published": 1748227306,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "KRX:KOSPI",
            "logoid": "indices/korea-composite-index"
          },
          {
            "symbol": "KRX:005930",
            "logoid": "samsung"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "KRX:373220",
            "logoid": "lg-energy-solution"
          },
          {
            "symbol": "KRX:006400",
            "logoid": "samsung"
          },
          {
            "symbol": "KRX:005380",
            "logoid": "hyundai"
          },
          {
            "symbol": "KRX:000270",
            "logoid": "kia"
          },
          {
            "symbol": "KRX:005490",
            "logoid": "posco"
          },
          {
            "symbol": "KRX:207940",
            "logoid": "samsung"
          },
          {
            "symbol": "FX_IDC:USDKRW",
            "currency-logoid": "country/KR",
            "base-currency-logoid": "country/US"
          },
          {
            "symbol": "TVC:KR10",
            "logoid": "country/KR"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L2N3RY01A:0-south-korean-shares-rise-1-as-trump-delays-eu-tariffs-battery-makers-rebound/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L6N3RY03H:0",
        "title": "Shares in China-listed Apple suppliers fall after Trump's tariff threats",
        "published": 1748225919,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "SZSE:002475",
            "logoid": "luxshare-precision"
          },
          {
            "symbol": "SZSE:300433",
            "logoid": "lens-technology-co"
          },
          {
            "symbol": "SZSE:002241",
            "logoid": "goertek-inc"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L6N3RY03H:0-shares-in-china-listed-apple-suppliers-fall-after-trump-s-tariff-threats/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L3N3RX060:0",
        "title": "Asian stocks, euro gain after Trump delays EU tariffs",
        "published": 1748225446,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "TVC:NI225",
            "logoid": "indices/nikkei-225"
          },
          {
            "symbol": "TSE:5401",
            "logoid": "nippon-steel-and-sumitomo-metal"
          },
          {
            "symbol": "SZSE:399300"
          },
          {
            "symbol": "HSI:HSI",
            "logoid": "indices/hang-seng"
          },
          {
            "symbol": "FX:EURUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "country/EU"
          },
          {
            "symbol": "FX_IDC:USDJPY",
            "currency-logoid": "country/JP",
            "base-currency-logoid": "country/US"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "TVC:GOLD",
            "logoid": "metal/gold"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L3N3RX060:0-asian-stocks-euro-gain-after-trump-delays-eu-tariffs/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_P8N3RE08L:0",
        "title": "Major China-listed Apple suppliers including Luxshare, Goertek fall after Trump's tariff threats",
        "published": 1748223047,
        "urgency": 1,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "SZSE:002475",
            "logoid": "luxshare-precision"
          },
          {
            "symbol": "SZSE:002241",
            "logoid": "goertek-inc"
          },
          {
            "symbol": "SZSE:300433",
            "logoid": "lens-technology-co"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_P8N3RE08L:0-major-china-listed-apple-suppliers-including-luxshare-goertek-fall-after-trump-s-tariff-threats/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L1N3RV0YF:0",
        "title": "Dollar, stocks fall as Trump targets Europe and Apple in tariff threats",
        "published": 1748036058,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "TVC:DXY",
            "logoid": "indices/u-s-dollar-index"
          },
          {
            "symbol": "FX_IDC:USDJPY",
            "currency-logoid": "country/JP",
            "base-currency-logoid": "country/US"
          },
          {
            "symbol": "FX:EURUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "country/EU"
          },
          {
            "symbol": "DJ:DJI",
            "logoid": "indices/dow-30"
          },
          {
            "symbol": "SP:SPX",
            "logoid": "indices/s-and-p-500"
          },
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "TVC:SXXP",
            "logoid": "indices/stoxx-600"
          },
          {
            "symbol": "TVC:US10Y",
            "logoid": "country/US"
          },
          {
            "symbol": "TVC:GOLD",
            "logoid": "metal/gold"
          },
          {
            "symbol": "ICEEUR:BRN1!",
            "logoid": "crude-oil"
          },
          {
            "symbol": "NYMEX:CL1!",
            "logoid": "crude-oil"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L1N3RV0YF:0-dollar-stocks-fall-as-trump-targets-europe-and-apple-in-tariff-threats/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L6N3RV0TC:0",
        "title": "Trump threatens new tariffs on European Union and Apple, reigniting trade fears",
        "published": 1748032101,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L6N3RV0TC:0-trump-threatens-new-tariffs-on-european-union-and-apple-reigniting-trade-fears/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L1N3RV0RW:0",
        "title": "Latam FX benefits from weak dollar after Trump's fresh tariff threat",
        "published": 1748032078,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "TVC:DXY",
            "logoid": "indices/u-s-dollar-index"
          },
          {
            "symbol": "FX_IDC:USDBRL",
            "currency-logoid": "country/BR",
            "base-currency-logoid": "country/US"
          },
          {
            "symbol": "BMFBOVESPA:IBOV"
          },
          {
            "symbol": "FX_IDC:USDCLP",
            "currency-logoid": "country/CL",
            "base-currency-logoid": "country/US"
          },
          {
            "symbol": "BCS:SP_IPSA",
            "logoid": "indices/s-and-p-ipsa"
          },
          {
            "symbol": "FX_IDC:USDCOP",
            "currency-logoid": "country/CO",
            "base-currency-logoid": "country/US"
          },
          {
            "symbol": "BVC:ICAP",
            "logoid": "indices/indice-bursatil-de-capitalizacion"
          },
          {
            "symbol": "FX_IDC:USDMXN",
            "currency-logoid": "country/MX",
            "base-currency-logoid": "country/US"
          },
          {
            "symbol": "BMV:ME",
            "logoid": "indices/ipc-mexico-index"
          },
          {
            "symbol": "BCBA:IMV",
            "logoid": "indices/merval-index"
          },
          {
            "symbol": "FX_IDC:USDPEN",
            "currency-logoid": "country/PE",
            "base-currency-logoid": "country/US"
          },
          {
            "symbol": "FX_IDC:USDARS",
            "currency-logoid": "country/AR",
            "base-currency-logoid": "country/US"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L1N3RV0RW:0-latam-fx-benefits-from-weak-dollar-after-trump-s-fresh-tariff-threat/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L1N3RV0W1:0",
        "title": "Wall St falls as Trump tariff threats spark market uncertainty",
        "published": 1748031725,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "DJ:DJI",
            "logoid": "indices/dow-30"
          },
          {
            "symbol": "SP:SPX",
            "logoid": "indices/s-and-p-500"
          },
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "TVC:VIX",
            "logoid": "country/US"
          },
          {
            "symbol": "NASDAQ:SOX",
            "logoid": "indices/philadelphia-semiconductor-index"
          },
          {
            "symbol": "NYSE:DECK",
            "logoid": "deckers-outdoor"
          },
          {
            "symbol": "NYSE:NKE",
            "logoid": "nike"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L1N3RV0W1:0-wall-st-falls-as-trump-tariff-threats-spark-market-uncertainty/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L6N3RV0T9:0",
        "title": "US stocks, roiled anew by tariff tensions, slide into Memorial Day weekend",
        "published": 1748031349,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "SP:S5INFT",
            "logoid": "sector/information-technology"
          },
          {
            "symbol": "NASDAQ:SOX",
            "logoid": "indices/philadelphia-semiconductor-index"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L6N3RV0T9:0-us-stocks-roiled-anew-by-tariff-tensions-slide-into-memorial-day-weekend/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L1N3RV0TJ:0",
        "title": "Dollar, stocks slip as Trump targets Europe and Apple in tariff threats",
        "published": 1748029074,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "TVC:DXY",
            "logoid": "indices/u-s-dollar-index"
          },
          {
            "symbol": "FX:EURUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "country/EU"
          },
          {
            "symbol": "FX_IDC:USDJPY",
            "currency-logoid": "country/JP",
            "base-currency-logoid": "country/US"
          },
          {
            "symbol": "DJ:DJI",
            "logoid": "indices/dow-30"
          },
          {
            "symbol": "SP:SPX",
            "logoid": "indices/s-and-p-500"
          },
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "TVC:SXXP",
            "logoid": "indices/stoxx-600"
          },
          {
            "symbol": "TVC:US10Y",
            "logoid": "country/US"
          },
          {
            "symbol": "TVC:GOLD",
            "logoid": "metal/gold"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L1N3RV0TJ:0-dollar-stocks-slip-as-trump-targets-europe-and-apple-in-tariff-threats/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L4N3RV168:0",
        "title": "Apple falls after Trump says 25% tariffs on iPhones not made in US",
        "published": 1748026082,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "KRX:005930",
            "logoid": "samsung"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L4N3RV168:0-apple-falls-after-trump-says-25-tariffs-on-iphones-not-made-in-us/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L1N3RV0KQ:0",
        "title": "Yields ease on growth concerns as Trump threatens more tariffs",
        "published": 1748025053,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "TVC:US10Y",
            "logoid": "country/US"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L1N3RV0KQ:0-yields-ease-on-growth-concerns-as-trump-threatens-more-tariffs/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_S0N3RE056:0",
        "title": "Trump says his tariffs on Apple will also apply to Samsung",
        "published": 1748024483,
        "urgency": 1,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "KRX:005930",
            "logoid": "samsung"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_S0N3RE056:0-trump-says-his-tariffs-on-apple-will-also-apply-to-samsung/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L1N3RV0O0:0",
        "title": "Reaction to Trump's threat of 50% tariffs on EU goods",
        "published": 1748016973,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "OMXSTO:VOLCAR_B",
            "logoid": "volvo-car"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L1N3RV0O0:0-reaction-to-trump-s-threat-of-50-tariffs-on-eu-goods/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L1N3RV0LW:0",
        "title": "Markets fall as Trump recommends 50% tariff on EU, targets Apple",
        "published": 1748016009,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "SP:SPX",
            "logoid": "indices/s-and-p-500"
          },
          {
            "symbol": "TVC:SXXP",
            "logoid": "indices/stoxx-600"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L1N3RV0LW:0-markets-fall-as-trump-recommends-50-tariff-on-eu-targets-apple/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L4N3RV0YY:0",
        "title": "Wall St falls after Trump threatens steep tariffs on EU, Apple",
        "published": 1748015373,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "DJ:DJI",
            "logoid": "indices/dow-30"
          },
          {
            "symbol": "SP:SPX",
            "logoid": "indices/s-and-p-500"
          },
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "TVC:VIX",
            "logoid": "country/US"
          },
          {
            "symbol": "SP:S5COND",
            "logoid": "sector/consumer-discretionary"
          },
          {
            "symbol": "SP:S5INFT",
            "logoid": "sector/information-technology"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:SOX",
            "logoid": "indices/philadelphia-semiconductor-index"
          },
          {
            "symbol": "NASDAQ:AAL",
            "logoid": "american-airlines-group"
          },
          {
            "symbol": "NYSE:DECK",
            "logoid": "deckers-outdoor"
          },
          {
            "symbol": "NYSE:NKE",
            "logoid": "nike"
          },
          {
            "symbol": "TVC:US10Y",
            "logoid": "country/US"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L4N3RV0YY:0-wall-st-falls-after-trump-threatens-steep-tariffs-on-eu-apple/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L1N3RV0IE:0",
        "title": "Bessent says Trump tariff threat may light a fire under EU in trade talks",
        "published": 1748012743,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L1N3RV0IE:0-bessent-says-trump-tariff-threat-may-light-a-fire-under-eu-in-trade-talks/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L4N3RV0WV:0",
        "title": "Latam stocks drop as Trump unleashes fresh tariff threats",
        "published": 1748012312,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "TVC:DXY",
            "logoid": "indices/u-s-dollar-index"
          },
          {
            "symbol": "FX_IDC:USDBRL",
            "currency-logoid": "country/BR",
            "base-currency-logoid": "country/US"
          },
          {
            "symbol": "BMFBOVESPA:IBOV"
          },
          {
            "symbol": "FX_IDC:USDCLP",
            "currency-logoid": "country/CL",
            "base-currency-logoid": "country/US"
          },
          {
            "symbol": "BCS:SP_IPSA",
            "logoid": "indices/s-and-p-ipsa"
          },
          {
            "symbol": "FX_IDC:USDCOP",
            "currency-logoid": "country/CO",
            "base-currency-logoid": "country/US"
          },
          {
            "symbol": "BCBA:IMV",
            "logoid": "indices/merval-index"
          },
          {
            "symbol": "BMV:ME",
            "logoid": "indices/ipc-mexico-index"
          },
          {
            "symbol": "FX_IDC:USDMXN",
            "currency-logoid": "country/MX",
            "base-currency-logoid": "country/US"
          },
          {
            "symbol": "BVC:ICAP",
            "logoid": "indices/indice-bursatil-de-capitalizacion"
          },
          {
            "symbol": "FX_IDC:USDPEN",
            "currency-logoid": "country/PE",
            "base-currency-logoid": "country/US"
          },
          {
            "symbol": "FX_IDC:USDARS",
            "currency-logoid": "country/AR",
            "base-currency-logoid": "country/US"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L4N3RV0WV:0-latam-stocks-drop-as-trump-unleashes-fresh-tariff-threats/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L1N3RV0FP:0",
        "title": "Trump's 50% tariff threat trims euro's gains against dollar",
        "published": 1748010749,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "TVC:DXY",
            "logoid": "indices/u-s-dollar-index"
          },
          {
            "symbol": "FX:EURUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "country/EU"
          },
          {
            "symbol": "FX_IDC:USDJPY",
            "currency-logoid": "country/JP",
            "base-currency-logoid": "country/US"
          },
          {
            "symbol": "FX:GBPUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "country/GB"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L1N3RV0FP:0-trump-s-50-tariff-threat-trims-euro-s-gains-against-dollar/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L4N3RV0W8:0",
        "title": "Wall St slumps about 1% after Trump threatens EU, Apple with fresh tariffs",
        "published": 1748009210,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "DJ:DJI",
            "logoid": "indices/dow-30"
          },
          {
            "symbol": "SP:SPX",
            "logoid": "indices/s-and-p-500"
          },
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "TVC:VIX",
            "logoid": "country/US"
          },
          {
            "symbol": "SP:S5COND",
            "logoid": "sector/consumer-discretionary"
          },
          {
            "symbol": "SP:S5INFT",
            "logoid": "sector/information-technology"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:SOX",
            "logoid": "indices/philadelphia-semiconductor-index"
          },
          {
            "symbol": "NASDAQ:AAL",
            "logoid": "american-airlines-group"
          },
          {
            "symbol": "NYSE:NKE",
            "logoid": "nike"
          },
          {
            "symbol": "NYSE:BBY",
            "logoid": "best-buy"
          },
          {
            "symbol": "NYSE:DECK",
            "logoid": "deckers-outdoor"
          },
          {
            "symbol": "TVC:US10Y",
            "logoid": "country/US"
          },
          {
            "symbol": "NASDAQ:INTU",
            "logoid": "intuit"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L4N3RV0W8:0-wall-st-slumps-about-1-after-trump-threatens-eu-apple-with-fresh-tariffs/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L8N3RV0W3:0",
        "title": "German minister: Trump tariffs help nobody, EU will continue talks",
        "published": 1748007936,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L8N3RV0W3:0-german-minister-trump-tariffs-help-nobody-eu-will-continue-talks/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L4N3RV0WY:0",
        "title": "Wall St falls at open after Trump threatens EU, Apple with fresh tariffs",
        "published": 1748007143,
        "urgency": 1,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "DJ:DJI",
            "logoid": "indices/dow-30"
          },
          {
            "symbol": "SP:SPX",
            "logoid": "indices/s-and-p-500"
          },
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L4N3RV0WY:0-wall-st-falls-at-open-after-trump-threatens-eu-apple-with-fresh-tariffs/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L6N3RV0KS:0",
        "title": "US asset managers fall as Trump re-ignites trade war fears",
        "published": 1748005765,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:IVZ",
            "logoid": "invesco"
          },
          {
            "symbol": "NYSE:APO",
            "logoid": "apollo"
          },
          {
            "symbol": "NYSE:BX",
            "logoid": "blackstone"
          },
          {
            "symbol": "NYSE:KKR",
            "logoid": "kkr"
          },
          {
            "symbol": "NYSE:SCHW",
            "logoid": "schwab"
          },
          {
            "symbol": "NYSE:BLK",
            "logoid": "blackrock"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L6N3RV0KS:0-us-asset-managers-fall-as-trump-re-ignites-trade-war-fears/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L4N3RV0UK:0",
        "title": "Wall St set to drop after Trump threatens EU, Apple with fresh tariffs",
        "published": 1748005532,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "CME_MINI:ES1!",
            "logoid": "indices/s-and-p-500"
          },
          {
            "symbol": "CME_MINI:NQ1!",
            "logoid": "indices/nasdaq-100"
          },
          {
            "symbol": "TVC:VIX",
            "logoid": "country/US"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:AMD",
            "logoid": "advanced-micro-devices"
          },
          {
            "symbol": "NASDAQ:INTC",
            "logoid": "intel"
          },
          {
            "symbol": "NASDAQ:AAL",
            "logoid": "american-airlines-group"
          },
          {
            "symbol": "NYSE:NKE",
            "logoid": "nike"
          },
          {
            "symbol": "NYSE:BBY",
            "logoid": "best-buy"
          },
          {
            "symbol": "NYSE:DECK",
            "logoid": "deckers-outdoor"
          },
          {
            "symbol": "TVC:US10Y",
            "logoid": "country/US"
          },
          {
            "symbol": "NASDAQ:INTU",
            "logoid": "intuit"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L4N3RV0UK:0-wall-st-set-to-drop-after-trump-threatens-eu-apple-with-fresh-tariffs/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L4N3RV0MO:0",
        "title": "US stock futures slump after Trump's EU, Apple tariffs threat",
        "published": 1748003280,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "CME_MINI:ES1!",
            "logoid": "indices/s-and-p-500"
          },
          {
            "symbol": "CME_MINI:NQ1!",
            "logoid": "indices/nasdaq-100"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "TVC:VIX",
            "logoid": "country/US"
          },
          {
            "symbol": "TVC:US10Y",
            "logoid": "country/US"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L4N3RV0MO:0-us-stock-futures-slump-after-trump-s-eu-apple-tariffs-threat/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L6N3RV0JB:0",
        "title": "US big banks fall as Trump tariffs resurface",
        "published": 1748002827,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:GS",
            "logoid": "golden-sachs-etf-trust-goldman"
          },
          {
            "symbol": "NYSE:JPM",
            "logoid": "jpmorgan-chase"
          },
          {
            "symbol": "NYSE:WFC",
            "logoid": "wells-fargo"
          },
          {
            "symbol": "NYSE:BAC",
            "logoid": "bank-of-america"
          },
          {
            "symbol": "NYSE:C",
            "logoid": "citigroup"
          },
          {
            "symbol": "NYSE:MS",
            "logoid": "morgan-stanley"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L6N3RV0JB:0-us-big-banks-fall-as-trump-tariffs-resurface/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L4N3RV0Q8:0",
        "title": "Trump threatens new tariffs on European Union, Apple, reigniting trade fears",
        "published": 1747999857,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L4N3RV0Q8:0-trump-threatens-new-tariffs-on-european-union-apple-reigniting-trade-fears/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L4N3RV0PW:0",
        "title": "Apple to pay 25% tariff if phones not made in US, Trump says",
        "published": 1747999607,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L4N3RV0PW:0-apple-to-pay-25-tariff-if-phones-not-made-in-us-trump-says/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_S0N3RE05E:0",
        "title": "Trump says Apple to pay 25% tariff on iPhones sold in the US, but not made in country",
        "published": 1747999307,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_S0N3RE05E:0-trump-says-apple-to-pay-25-tariff-on-iphones-sold-in-the-us-but-not-made-in-country/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L4N3RV0HV:0",
        "title": "European stocks close week lower on Trump's EU, Apple tariff threats",
        "published": 1747990847,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "TVC:SXXP",
            "logoid": "indices/stoxx-600"
          },
          {
            "symbol": "XETR:DAX",
            "logoid": "indices/dax"
          },
          {
            "symbol": "EURONEXT:PX1",
            "logoid": "indices/cac-40"
          },
          {
            "symbol": "BME:IBC",
            "logoid": "indices/ibex-35"
          },
          {
            "symbol": "INDEX:FTSEMIB",
            "logoid": "indices/ftse-mib"
          },
          {
            "symbol": "TVC:US10Y",
            "logoid": "country/US"
          },
          {
            "symbol": "LSE:AJB",
            "logoid": "aj-bell-plc"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L4N3RV0HV:0-european-stocks-close-week-lower-on-trump-s-eu-apple-tariff-threats/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L6N3RR0AZ:0",
        "title": "The post-truce state of US-China trade looks dire",
        "published": 1747656023,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "SZSE:399300"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "HKEX:303",
            "logoid": "vtech-ltd"
          },
          {
            "symbol": "NYSE:WMT"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L6N3RR0AZ:0-the-post-truce-state-of-us-china-trade-looks-dire/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L4N3RM142:0",
        "title": "US smartphone shipments rose 30% in March due to tariff concerns, report says",
        "published": 1747228381,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "KRX:005930",
            "logoid": "samsung"
          },
          {
            "symbol": "HKEX:80992",
            "logoid": "lenovo"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L4N3RM142:0-us-smartphone-shipments-rose-30-in-march-due-to-tariff-concerns-report-says/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L1N3RL0FV:0",
        "title": "UK chips supplier IQE could move some production to US on tariff concerns",
        "published": 1747139586,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "LSE:IQE",
            "logoid": "iqe-plc"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L1N3RL0FV:0-uk-chips-supplier-iqe-could-move-some-production-to-us-on-tariff-concerns/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L6N3RA0BQ:0",
        "title": "Street View: India is Apple's \"life raft supply chain\" in trade war",
        "published": 1746177091,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L6N3RA0BQ:0-street-view-india-is-apple-s-life-raft-supply-chain-in-trade-war/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L6N3R90J0:0",
        "title": "Apple girds for more trade war pain, trims buyback",
        "published": 1746131777,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L6N3R90J0:0-apple-girds-for-more-trade-war-pain-trims-buyback/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L1N3R90AC:0",
        "title": "Big Tech's fortunes diverge as AI powers cloud, tariffs hit consumer electronics",
        "published": 1746095129,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:QCOM",
            "logoid": "qualcomm"
          },
          {
            "symbol": "KRX:005930",
            "logoid": "samsung"
          },
          {
            "symbol": "NASDAQ:INTC",
            "logoid": "intel"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NYSE:SNAP",
            "logoid": "snap"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:AMD",
            "logoid": "advanced-micro-devices"
          },
          {
            "symbol": "NASDAQ:AVGO",
            "logoid": "broadcom"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L1N3R90AC:0-big-tech-s-fortunes-diverge-as-ai-powers-cloud-tariffs-hit-consumer-electronics/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L6N3QS0MO:0",
        "title": "KeyBanc upgrades Apple on smartphone tariff exemption but growth concerns remain",
        "published": 1744649135,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L6N3QS0MO:0-keybanc-upgrades-apple-on-smartphone-tariff-exemption-but-growth-concerns-remain/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L4N3QQ01D:0",
        "title": "Bullish trade in Apple options reaps gains as shares jump on tariff exemption",
        "published": 1744641917,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "AMEX:SPY",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NDX",
            "logoid": "indices/nasdaq-100"
          },
          {
            "symbol": "CBOE:SPX",
            "logoid": "indices/s-and-p-500"
          },
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L4N3QQ01D:0-bullish-trade-in-apple-options-reaps-gains-as-shares-jump-on-tariff-exemption/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L1N3QS03D:0",
        "title": "Asian tech stocks bounce back after Trump tariff exemptions",
        "published": 1744601777,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "TWSE:2317",
            "logoid": "hon-hai"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "TWSE:2382",
            "logoid": "quanta-computer"
          },
          {
            "symbol": "TWSE:2356",
            "logoid": "inventec"
          },
          {
            "symbol": "SZSE:002241",
            "logoid": "goertek-inc"
          },
          {
            "symbol": "SZSE:300433",
            "logoid": "lens-technology-co"
          },
          {
            "symbol": "KRX:005930",
            "logoid": "samsung"
          },
          {
            "symbol": "TWSE:2330",
            "logoid": "taiwan-semiconductor"
          },
          {
            "symbol": "KRX:000660",
            "logoid": "sk-telecom"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L1N3QS03D:0-asian-tech-stocks-bounce-back-after-trump-tariff-exemptions/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L1N3QS02W:0",
        "title": "Taiwan tech supply chain stocks bounce back after Trump tariff exemptions",
        "published": 1744597798,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "TWSE:2317",
            "logoid": "hon-hai"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "TWSE:2382",
            "logoid": "quanta-computer"
          },
          {
            "symbol": "TWSE:2356",
            "logoid": "inventec"
          },
          {
            "symbol": "TWSE:2330",
            "logoid": "taiwan-semiconductor"
          },
          {
            "symbol": "TWSE:2354",
            "logoid": "foxconn-tech-co"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L1N3QS02W:0-taiwan-tech-supply-chain-stocks-bounce-back-after-trump-tariff-exemptions/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L1N3QQ03D:0",
        "title": "Trump spares smartphones, computers, other electronics from China tariffs",
        "published": 1744480647,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:DELL",
            "logoid": "dell"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "TWSE:2330",
            "logoid": "taiwan-semiconductor"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L1N3QQ03D:0-trump-spares-smartphones-computers-other-electronics-from-china-tariffs/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L3N3QH1ZG:0",
        "title": "What Samsung and Vietnam stand to lose in Trump's tariff war",
        "published": 1744426749,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "KRX:005930",
            "logoid": "samsung"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L3N3QH1ZG:0-what-samsung-and-vietnam-stand-to-lose-in-trump-s-tariff-war/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L3N3QN1VA:0",
        "title": "Apple airlifts 600 tons of iPhones from India 'to beat' Trump tariffs, sources say",
        "published": 1744275234,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "isExclusive": true,
        "storyPath": "/news/reuters.com,2025:newsml_L3N3QN1VA:0-apple-airlifts-600-tons-of-iphones-from-india-to-beat-trump-tariffs-sources-say/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L3N3QN1WR:0",
        "title": "Big Tech rises after Trump announces 90-day pause on tariffs excluding China",
        "published": 1744223353,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NYSE:JPM",
            "logoid": "jpmorgan-chase"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L3N3QN1WR:0-big-tech-rises-after-trump-announces-90-day-pause-on-tariffs-excluding-china/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L3N3QN1JH:0",
        "title": "Apple rises as Jefferies upgrades to 'hold' on hopes of tariff exemption",
        "published": 1744207156,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L3N3QN1JH:0-apple-rises-as-jefferies-upgrades-to-hold-on-hopes-of-tariff-exemption/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L6N3QN0D1:0",
        "title": "Apple rises as Jefferies upgrades to 'Hold' on anticipation of tariff exemption",
        "published": 1744194118,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L6N3QN0D1:0-apple-rises-as-jefferies-upgrades-to-hold-on-anticipation-of-tariff-exemption/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L3N3QI0QP:0",
        "title": "Tesla, chips, and banks tumble as China's retaliation stokes fears of widening trade war",
        "published": 1743776557,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:GEHC",
            "logoid": "ge-healthcare-technologies"
          },
          {
            "symbol": "NASDAQ:INTC",
            "logoid": "intel"
          },
          {
            "symbol": "NASDAQ:AMAT",
            "logoid": "applied-materials"
          },
          {
            "symbol": "NASDAQ:QCOM",
            "logoid": "qualcomm"
          },
          {
            "symbol": "NYSE:XOM",
            "logoid": "exxon"
          },
          {
            "symbol": "NYSE:CVX",
            "logoid": "chevron"
          },
          {
            "symbol": "NYSE:SLB",
            "logoid": "schlumberger"
          },
          {
            "symbol": "NYSE:MPC",
            "logoid": "marathon-petroleum"
          },
          {
            "symbol": "NYSE:DD",
            "logoid": "dupont-de-nemours"
          },
          {
            "symbol": "NYSE:ADM",
            "logoid": "archer-daniels-midland"
          },
          {
            "symbol": "NYSE:BG",
            "logoid": "bunge"
          },
          {
            "symbol": "NYSE:MOS",
            "logoid": "mosaic"
          },
          {
            "symbol": "NYSE:CF",
            "logoid": "cf-industries"
          },
          {
            "symbol": "NYSE:JPM",
            "logoid": "jpmorgan-chase"
          },
          {
            "symbol": "NYSE:GS",
            "logoid": "golden-sachs-etf-trust-goldman"
          },
          {
            "symbol": "NYSE:MS",
            "logoid": "morgan-stanley"
          },
          {
            "symbol": "NYSE:CAT",
            "logoid": "caterpillar"
          },
          {
            "symbol": "NYSE:DE",
            "logoid": "deere"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L3N3QI0QP:0-tesla-chips-and-banks-tumble-as-china-s-retaliation-stokes-fears-of-widening-trade-war/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L3N3QI0UH:0",
        "title": "Big Tech stocks fall after China retaliates with 34% additional import tariffs on US goods",
        "published": 1743775238,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L3N3QI0UH:0-big-tech-stocks-fall-after-china-retaliates-with-34-additional-import-tariffs-on-us-goods/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L3N3QI0IG:0",
        "title": "Nasdaq set to confirm bear market as Trump tariffs trigger recession fears",
        "published": 1743773431,
        "urgency": 1,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "TVC:DJI",
            "logoid": "indices/dow-30"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "CBOE:SPX",
            "logoid": "indices/s-and-p-500"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L3N3QI0IG:0-nasdaq-set-to-confirm-bear-market-as-trump-tariffs-trigger-recession-fears/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L3N3QI0P3:0",
        "title": "Tech, bank stocks bear the brunt as China retaliates to Trump tariffs",
        "published": 1743769552,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NYSE:JPM",
            "logoid": "jpmorgan-chase"
          },
          {
            "symbol": "NYSE:GS",
            "logoid": "golden-sachs-etf-trust-goldman"
          },
          {
            "symbol": "NYSE:MS",
            "logoid": "morgan-stanley"
          },
          {
            "symbol": "NYSE:XOM",
            "logoid": "exxon"
          },
          {
            "symbol": "NYSE:CVX",
            "logoid": "chevron"
          },
          {
            "symbol": "NYSE:SLB",
            "logoid": "schlumberger"
          },
          {
            "symbol": "NYSE:MPC",
            "logoid": "marathon-petroleum"
          },
          {
            "symbol": "NASDAQ:GEHC",
            "logoid": "ge-healthcare-technologies"
          },
          {
            "symbol": "NYSE:F",
            "logoid": "ford"
          },
          {
            "symbol": "NYSE:GM",
            "logoid": "general-motors"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L3N3QI0P3:0-tech-bank-stocks-bear-the-brunt-as-china-retaliates-to-trump-tariffs/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L3N3QI0LG:0",
        "title": "Big Tech stocks fall after China retaliates with 34% import tariffs on US goods",
        "published": 1743763417,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L3N3QI0LG:0-big-tech-stocks-fall-after-china-retaliates-with-34-import-tariffs-on-us-goods/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L6N3QH0TG:0",
        "title": "A $2,300 Apple iPhone? Trump tariffs could make that happen",
        "published": 1743698952,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "KRX:005930",
            "logoid": "samsung"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L6N3QH0TG:0-a-2-300-apple-iphone-trump-tariffs-could-make-that-happen/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L3N3QH1HG:0",
        "title": "Will Trump tariffs make Apple iPhones more expensive?",
        "published": 1743697513,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "KRX:005930",
            "logoid": "samsung"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L3N3QH1HG:0-will-trump-tariffs-make-apple-iphones-more-expensive/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L3N3QH1BC:0",
        "title": "Apple hits 8-mth low as analysts warn Trump's tariffs to squeeze profits",
        "published": 1743689604,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "KRX:005930",
            "logoid": "samsung"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L3N3QH1BC:0-apple-hits-8-mth-low-as-analysts-warn-trump-s-tariffs-to-squeeze-profits/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L3N3QH0P7:0",
        "title": "Apple's $500 billion US investment may help secure tariff exemptions, Jefferies says",
        "published": 1743668240,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L3N3QH0P7:0-apple-s-500-billion-us-investment-may-help-secure-tariff-exemptions-jefferies-says/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L3N3QG1F9:0",
        "title": "Big Tech companies fall after Trump's reciprocal tariffs",
        "published": 1743630389,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L3N3QG1F9:0-big-tech-companies-fall-after-trump-s-reciprocal-tariffs/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L3N3QG1ER:0",
        "title": "Apple falls after Trump imposes reciprocal tariffs",
        "published": 1743628987,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L3N3QG1ER:0-apple-falls-after-trump-imposes-reciprocal-tariffs/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L3N3QF0VO:0",
        "title": "Trump tariffs triggered big Q1 plunge in market values for top global firms",
        "published": 1743508232,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:AVGO",
            "logoid": "broadcom"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "TWSE:2330",
            "logoid": "taiwan-semiconductor"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L3N3QF0VO:0-trump-tariffs-triggered-big-q1-plunge-in-market-values-for-top-global-firms/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_P8N3OC06K:0",
        "title": "China trade council says welcomes Apple to deepen supply-chain cooperation",
        "published": 1742785371,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_P8N3OC06K:0-china-trade-council-says-welcomes-apple-to-deepen-supply-chain-cooperation/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L4N3Q40RT:0",
        "title": "How companies are responding to Trump's tariffs",
        "published": 1742555741,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NYSE:BBY",
            "logoid": "best-buy"
          },
          {
            "symbol": "NYSE:TGT",
            "logoid": "target"
          },
          {
            "symbol": "NYSE:KR",
            "logoid": "kroger"
          },
          {
            "symbol": "NASDAQ:COST",
            "logoid": "costco-wholesale"
          },
          {
            "symbol": "NYSE:AA",
            "logoid": "alcoa"
          },
          {
            "symbol": "NYSE:HPE",
            "logoid": "hewlett-packard-enterprise"
          },
          {
            "symbol": "TSE:7267",
            "logoid": "honda"
          },
          {
            "symbol": "NYSE:PFE",
            "logoid": "pfizer"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:LLY",
            "logoid": "eli-lilly"
          },
          {
            "symbol": "NYSE:JNJ",
            "logoid": "johnson-and-johnson"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L4N3Q40RT:0-how-companies-are-responding-to-trump-s-tariffs/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L4N3Q40PE:0",
        "title": "J&J boosts US investments by 25% over 4 years amid looming tariff threats",
        "published": 1742551933,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NYSE:JNJ",
            "logoid": "johnson-and-johnson"
          },
          {
            "symbol": "NYSE:LLY",
            "logoid": "eli-lilly"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:PFE",
            "logoid": "pfizer"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L4N3Q40PE:0-j-j-boosts-us-investments-by-25-over-4-years-amid-looming-tariff-threats/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L6N3PO0W6:0",
        "title": "Sony, Suntory build U.S. stockpiles as Japan faces Trump tariff threat",
        "published": 1741216836,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "TSE:7267",
            "logoid": "honda"
          },
          {
            "symbol": "TSE:6740",
            "logoid": "japan-display"
          },
          {
            "symbol": "TSE:6770",
            "logoid": "alps-alpine-co-ltd"
          },
          {
            "symbol": "TSE:6981",
            "logoid": "murata-manufacturing"
          },
          {
            "symbol": "TSE:6758",
            "logoid": "sony"
          },
          {
            "symbol": "TSE:2587",
            "logoid": "suntory"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L6N3PO0W6:0-sony-suntory-build-u-s-stockpiles-as-japan-faces-trump-tariff-threat/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L4N3OX0JC:0",
        "title": "Trump tariff effect boosts Taiwan's January exports",
        "published": 1738920528,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "TWSE:2330",
            "logoid": "taiwan-semiconductor"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L4N3OX0JC:0-trump-tariff-effect-boosts-taiwan-s-january-exports/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L4N3OU183:0",
        "title": "Apple's profit to see 'limited impact' from US tariffs on China, BofA says",
        "published": 1738595605,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L4N3OU183:0-apple-s-profit-to-see-limited-impact-from-us-tariffs-on-china-bofa-says/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L4N3OU0QO:0",
        "title": "Car makers, brewers pare losses as Trump pauses tariffs on Mexico",
        "published": 1738588479,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "AMEX:EWW",
            "logoid": "ishares"
          },
          {
            "symbol": "NYSE:APTV",
            "logoid": "aptiv"
          },
          {
            "symbol": "NYSE:GM",
            "logoid": "general-motors"
          },
          {
            "symbol": "NYSE:F",
            "logoid": "ford"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NYSE:STZ",
            "logoid": "constellation-brands"
          },
          {
            "symbol": "NYSE:CCJ",
            "logoid": "cameco"
          },
          {
            "symbol": "TVC:RUT",
            "logoid": "indices/russell-2000"
          },
          {
            "symbol": "NASDAQ:COIN",
            "logoid": "coinbase"
          },
          {
            "symbol": "BITSTAMP:BTCUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "crypto/XTVCBTC"
          },
          {
            "symbol": "AMEX:EWZ",
            "logoid": "ishares"
          },
          {
            "symbol": "AMEX:UUUU",
            "logoid": "energy-fuels"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:CEG",
            "logoid": "constellation-energy-cad-hedged-cibc-cdr"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:PDD",
            "logoid": "pinduoduo"
          },
          {
            "symbol": "NYSE:BABA",
            "logoid": "alibaba"
          },
          {
            "symbol": "NYSE:VST",
            "logoid": "vistra-energy"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L4N3OU0QO:0-car-makers-brewers-pare-losses-as-trump-pauses-tariffs-on-mexico/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L3N3OR13G:0",
        "title": "TSX set for weekly gain despite concerns over looming US tariffs",
        "published": 1738339085,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "TSX:TSX",
            "logoid": "indices/s-and-p-tsx-composite-index"
          },
          {
            "symbol": "TSX:TTTK"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "TSX:TTEN",
            "logoid": "sector/energy"
          },
          {
            "symbol": "TSX:IMO",
            "logoid": "imperial-oil"
          },
          {
            "symbol": "TSX:NA",
            "logoid": "national-bank-of-canada"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L3N3OR13G:0-tsx-set-for-weekly-gain-despite-concerns-over-looming-us-tariffs/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      }
    ],
    "streaming": {
      "channel": "e704e17892b81c1cf92834d1e355"
    }
  },
  "msg": "Success"
}
```

## Get ETF News

`GET /api/news/etf`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/api/news/etf?symbol=NASDAQ%3AAAPL&lang=en' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "stocktwits:9cafd3a72094b:0",
        "title": "Nasdaq, S&P 500 Futures Steady As Iran Talks, Warsh Hearing Set Market Tone: Why AAPL, AMZN, POET, FRMI, IBRX Are In Focus",
        "published": 1776760781,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/nasdaq-sp500-futures-rise-aapl-amzn-poet-frmi-ibrx-stocks-to-watch/cZBIfgmRICh",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "BCBA:SPY",
            "logoid": "spdr-sandp500-etf-tr"
          }
        ],
        "storyPath": "/news/stocktwits:9cafd3a72094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "stocktwits:5692ebe19094b:0",
        "title": "Apple's New CEO Led A Silicon 'Brain Transplant' — Analyst Says That's Exactly Why John Ternus Is Right For Next AI Phase",
        "published": 1776757050,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-s-new-ceo-led-a-silicon-brain-transplant-analyst-says-that-s-exactly-why-john-ternus-is-right-for-next-ai-phase/cZBI9pwRICa",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:5692ebe19094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "stocktwits:99c909d7b094b:0",
        "title": "Apple After Tim Cook: Analysts See Continuity Pick, Not Vision Play Under New CEO John Ternus",
        "published": 1776740903,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-after-tim-cook-analysts-see-continuity-pick-not-vision-play-under-new-ceo-john-ternus/cZBIPluRIzz",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:99c909d7b094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "stocktwits:7499a5168094b:0",
        "title": "Is Himax A ‘Stealth’ Supplier To Nvidia, Apple? HIMX Stock Pops To Nearly 1-Year High After Hedge Fund Flags Possible Links",
        "published": 1773368534,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/is-himax-a-stealth-supplier-to-nvidia-apple-himx-stock-pops-to-nearly-1-year-high-after-hedge-fund-flags-possible-links/cZdwxZ1RIaB",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:HIMX",
            "logoid": "himax-technologies"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/stocktwits:7499a5168094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_DN20260306006471:0",
        "title": "3 Dividend ETFs for Shelter in These Stormy Times — Barrons.com",
        "published": 1772820900,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AVGO",
            "logoid": "broadcom"
          },
          {
            "symbol": "NYSE:KO",
            "logoid": "coca-cola"
          },
          {
            "symbol": "NYSE:COP",
            "logoid": "conocophillips"
          },
          {
            "symbol": "NYSE:LMT",
            "logoid": "lockheed-martin"
          }
        ],
        "storyPath": "/news/DJN_DN20260306006471:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "zacks:95b44c055094b:0",
        "title": "Budget iPhone 17e to Boost Apple Revenues? ETFs to Consider",
        "published": 1772641740,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2878814/budget-iphone-17e-to-boost-apple-revenues-etfs-to-consider?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2878814",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/zacks:95b44c055094b:0-budget-iphone-17e-to-boost-apple-revenues-etfs-to-consider/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "stocktwits:930831ece094b:0",
        "title": "Apple Launches MacBook Neo At $599, Offering An Alternative To Google’s Chromebooks",
        "published": 1772639380,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-launches-macbook-neo-starting-at-599-taking-on-google-chromebooks/cZd9YtyRI5z",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:930831ece094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_DN20260303008032:0",
        "title": "This Schwab Dividend ETF is a Superstar. Defense and Energy Are Key — Barrons.com",
        "published": 1772566800,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AVGO",
            "logoid": "broadcom"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:MORN",
            "logoid": "morningstar"
          }
        ],
        "storyPath": "/news/DJN_DN20260303008032:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:a55a75590094b:0",
        "title": "Apple’s AI Woes Meet A ‘Tsunami-Like’ Shock: IDC Sees Smartphone Shipments Crashing This Year",
        "published": 1772178224,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-s-ai-woes-meet-a-tsunami-like-shock-idc-sees-smartphone-shipments-crashing-this-year/cZTc9VjRIRH",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:a55a75590094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_SN20260226013776:0",
        "title": "These S&P 500 alternatives have shined so far this year",
        "published": 1772122560,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "CBOE:SPX",
            "logoid": "indices/s-and-p-500"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "AMEX:RSP",
            "logoid": "invesco"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/DJN_SN20260226013776:0/",
        "provider": {
          "id": "market-watch",
          "name": "MarketWatch",
          "logo_id": "marketwatch"
        }
      },
      {
        "id": "DJN_SN20260218015386:0",
        "title": "'Magnificent Seven' stocks rise - but hardly enough to reverse a brutal February",
        "published": 1771472460,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "CBOE:MAGS",
            "logoid": "roundhmetave-aeoa"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          }
        ],
        "storyPath": "/news/DJN_SN20260218015386:0/",
        "provider": {
          "id": "market-watch",
          "name": "MarketWatch",
          "logo_id": "marketwatch"
        }
      },
      {
        "id": "stocktwits:07fcf37b9094b:0",
        "title": "Nasdaq, S&P 500 Futures Edge Higher Ahead Of Fed Minutes: Why NVDA, TSLA, AAPL, APLD, PANW Are On Traders' Radar Today",
        "published": 1771404536,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/nasdaq-sp500-futures-higher-nvda-tsla-panw-apld-mltx-stocks-to-watch/cZR0mRsR4Hq",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/stocktwits:07fcf37b9094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "stocktwits:539bb33b3094b:0",
        "title": "Apple Eyeing Meta And Snap’s Turf? 3 New AI Gadgets Reportedly In Works",
        "published": 1771396383,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-eyeing-meta-and-snap-s-turf-3-new-ai-gadgets-reportedly-in-works/cZR0Ki3R4Hk",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:539bb33b3094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "stocktwits:a7a33263d094b:0",
        "title": "Nasdaq, S&P 500 Futures Lower As AI Disruption Fears Linger: Why AAPL, ZIM, OCUL, NCLH Are On Traders' Radar Today",
        "published": 1771317064,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/nasdaq-sp500-futures-slip-aapl-zim-ocul-nclh-stocks-to-watch/cZRWXi1R4MU",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NYSE:NCLH",
            "logoid": "norwegian-cruise-line"
          },
          {
            "symbol": "NYSE:ZIM",
            "logoid": "zim-integrated-shipping"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:a7a33263d094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "stocktwits:4a7f6eadb094b:0",
        "title": "Apple Expected To Debut Low-Cost MacBook, iPhone 17e At March 4 Event – Analyst Expects Small, Short Bump In Sales",
        "published": 1771298616,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-expected-to-debut-low-cost-macbook-iphone-17e-at-march-event/cZRW37FR4Mj",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:4a7f6eadb094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "stocktwits:f77bc6edb094b:0",
        "title": "Dow, S&P 500, Nasdaq Futures Rise On AI, Fed Watch After Holiday Break: Why ZIM, AAPL, TCNNF, DIS Kept Traders On Edge Today",
        "published": 1771292369,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/dow-sp500-nasdaq-futures-rise-ai-fed-watch-zim-aapl-tcnnf-dis/cZRWcirR4ML",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NYSE:DIS",
            "logoid": "walt-disney"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:ZIM",
            "logoid": "zim-integrated-shipping"
          }
        ],
        "storyPath": "/news/stocktwits:f77bc6edb094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "stocktwits:22a0c439d094b:0",
        "title": "Nasdaq, S&P 500 Futures Edge Lower Ahead Of CPI Data: Why NVDA, AAPL, TSLA, RIVN, MRNA, AMAT, IREN Are On Traders' Radar Today",
        "published": 1770973672,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/nasdaq-sp500-futures-lower-nvda-aapl-tsla-rivn-mrna-amat-stocks-to-watch/cZR5NHpR4sZ",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:RIVN",
            "logoid": "rivian"
          },
          {
            "symbol": "NASDAQ:QQQ",
            "logoid": "invesco"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMAT",
            "logoid": "applied-materials"
          },
          {
            "symbol": "BCBA:SPY",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:MRNA",
            "logoid": "moderna"
          }
        ],
        "storyPath": "/news/stocktwits:22a0c439d094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "stocktwits:f33658f01094b:0",
        "title": "Apple Stock Posts Worst Day In 10 Months On AI Setback, Regulatory Heat",
        "published": 1770966380,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-stock-posts-worst-day-in-10-months-on-ai-setback-regulatory-heat/cZR5jVGR4sL",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:f33658f01094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "stocktwits:d7eb949b8094b:0",
        "title": "Apple Stock Loses Retail Euphoria After Blowout Earnings; Will New AI Siri Reignite Confidence?",
        "published": 1770610027,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-stock-loses-retail-euphoria-after-blowout-earnings-will-new-ai-siri-reignite-confidence/cZbHVJhR48L",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:d7eb949b8094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "stocktwits:a52a81d6a094b:0",
        "title": "Apple Stock Is Bucking The Trillion-Dollar Tech Rout — But Caution Still Prevails On Retail Street",
        "published": 1770354874,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-stock-is-bucking-the-trillion-dollar-tech-rout/cZbFcNfR4n1",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:a52a81d6a094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "stocktwits:f3dc7dad4094b:0",
        "title": "What Does Apple’s Cook Think About The Immigration Issue In America?",
        "published": 1770323708,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/what-does-apple-cook-think-about-the-immigration-issue-in-america/cZbZjbPR4nd",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:f3dc7dad4094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "zacks:8d5bbf2a0094b:0",
        "title": "Should You Bet on Apple's iPhone-Driven Q1 Earnings? ETFs in Focus",
        "published": 1769781600,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2825980/should-you-bet-on-apple-s-iphone-driven-q1-earnings-etfs-in-focus?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2825980",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/zacks:8d5bbf2a0094b:0-should-you-bet-on-apple-s-iphone-driven-q1-earnings-etfs-in-focus/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "leverage_shares:9f1c1add6094b:0",
        "title": "Apple Posts a Blockbuster Q1 on iPhone Strength",
        "published": 1769779680,
        "urgency": 2,
        "link": "https://leverageshares.com/en-eu/insights/apple-posts-a-blockbuster-q1-on-iphone-strength/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/leverage_shares:9f1c1add6094b:0-apple-posts-a-blockbuster-q1-on-iphone-strength/",
        "provider": {
          "id": "leverage_shares",
          "name": "Leverage Shares",
          "logo_id": "leverage-shares",
          "url": "https://leverageshares.com/en/"
        }
      },
      {
        "id": "stocktwits:f803a70dc094b:0",
        "title": "Nasdaq, S&P 500 Futures Climb Ahead Of Apple Earnings: Why META, TSLA, MP, CRML, SER Are On Traders' Radar Today",
        "published": 1769676372,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/nasdaq-sp500-futures-higher-meta-tsla-ser-mp-crml-stocks-to-watch/cmyidGCR4KJ",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          }
        ],
        "storyPath": "/news/stocktwits:f803a70dc094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "stocktwits:96d9edc25094b:0",
        "title": "Apple Stock Poised For A Lift? iPhone 17 Seen Driving Best Holiday-Quarter Growth In 4 Years — But Margin Jitters Linger",
        "published": 1769672173,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-stock-poised-for-a-lift-iphone-17-seen-driving-best-holiday-quarter-growth-in-4-years/cmyi23mR4KE",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:96d9edc25094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "zacks:2d059794f094b:0",
        "title": "Apple-Heavy ETFs in Focus as iPhone Sales Power Holiday Quarter",
        "published": 1769616900,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2824511/apple-heavy-etfs-in-focus-as-iphone-sales-power-holiday-quarter?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2824511",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/zacks:2d059794f094b:0-apple-heavy-etfs-in-focus-as-iphone-sales-power-holiday-quarter/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:e891325b4094b:0",
        "title": " What Lies Ahead of Mag-7 Earnings? ETFs in Focus ",
        "published": 1769612400,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2824430/what-lies-ahead-of-mag-7-earnings-etfs-in-focus?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2824430",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/zacks:e891325b4094b:0-what-lies-ahead-of-mag-7-earnings-etfs-in-focus/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "stocktwits:71d5d0014094b:0",
        "title": "Trump Signals Military Escalation Toward Iran As Markets Brace For Big Tech Earnings, Fed Decision",
        "published": 1769604955,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/trump-signals-military-escalation-toward-iran-as-markets-brace-for-big-tech-earnings-fed-decision/cmygPjOR40T",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          }
        ],
        "storyPath": "/news/stocktwits:71d5d0014094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "stocktwits:a82d23c03094b:0",
        "title": "Dow, S&P 500, Nasdaq Futures Mixed As Investors Brace For More Big Tech Earnings, Fed Policy Update",
        "published": 1769491118,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/dow-s-and-p-500-nasdaq-futures-mixed-as-investors-brace-for-more-big-tech-earnings-fed-policy-update/cmyaNIaR4hH",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NDAQ",
            "logoid": "nasdaq"
          }
        ],
        "storyPath": "/news/stocktwits:a82d23c03094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "stocktwits:73446c3fc094b:0",
        "title": "Apple’s Siri Makeover Could Be The AI Catalyst Bulls Are Waiting For: Analyst",
        "published": 1769065700,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apples-siri-makeover-could-be-the-ai-catalyst-bulls-are-waiting-for/cmUzYhaR4QX",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:73446c3fc094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_SN20260121013352:0",
        "title": "Big Tech stocks haven't been this cheap in months. These investors say it's time to buy.",
        "published": 1769035200,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "CBOE:MAGS",
            "logoid": "roundhmetave-aeoa"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "AMEX:SPY",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          }
        ],
        "storyPath": "/news/DJN_SN20260121013352:0/",
        "provider": {
          "id": "market-watch",
          "name": "MarketWatch",
          "logo_id": "marketwatch"
        }
      },
      {
        "id": "stocktwits:9b93025fe094b:0",
        "title": "Apple Stock Lags ‘Mag 7’ Peers: Analyst Sees ‘Solid’ iPhone Revenue Amid Risk Of Higher Memory Costs",
        "published": 1768968968,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-stock-lags-mag-7-peers-analyst-sees-solid-iphone-revenue/cmUDg8PR4OF",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:9b93025fe094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "zacks:b9127e6e9094b:0",
        "title": "Siri to Get Smarter With Gemini: The ETF Playbook for Investors",
        "published": 1768493100,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2818228/siri-to-get-smarter-with-gemini-the-etf-playbook-for-investors?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2818228",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          }
        ],
        "storyPath": "/news/zacks:b9127e6e9094b:0-siri-to-get-smarter-with-gemini-the-etf-playbook-for-investors/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:0137c3404094b:0",
        "title": "ETFs to Gain as Alphabet Beats Apple in Market Capitalization",
        "published": 1767884160,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2814349/etfs-to-gain-as-alphabet-beats-apple-in-market-capitalization?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2814349",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          }
        ],
        "storyPath": "/news/zacks:0137c3404094b:0-etfs-to-gain-as-alphabet-beats-apple-in-market-capitalization/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:d4b79289a094b:0",
        "title": "Positioning for 2026: Market Outlook and ETF Strategies",
        "published": 1765832640,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2804646/positioning-for-2026-market-outlook-and-etf-strategies?cid=CS-TRADINGVIEW-FT-etf_spotlight-2804646",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "AMEX:GLD",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "AMEX:SPYG",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "AMEX:SPEM",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "AMEX:GLDM",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "AMEX:IAUM",
            "logoid": "ishares"
          }
        ],
        "storyPath": "/news/zacks:d4b79289a094b:0-positioning-for-2026-market-outlook-and-etf-strategies/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:814268de4094b:0",
        "title": "Top-Ranked ETFs to Power Your Portfolio Higher ",
        "published": 1765209180,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2801083/top-ranked-etfs-to-power-your-portfolio-higher?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2801083",
        "relatedSymbols": [
          {
            "symbol": "NYSE:JPM",
            "logoid": "jpmorgan-chase"
          },
          {
            "symbol": "NYSE:V",
            "logoid": "visa"
          },
          {
            "symbol": "NYSE:JNJ",
            "logoid": "johnson-and-johnson"
          },
          {
            "symbol": "NYSE:LLY",
            "logoid": "eli-lilly"
          },
          {
            "symbol": "NYSE:SHW",
            "logoid": "sherwin-williams"
          },
          {
            "symbol": "NYSE:BRK.A",
            "logoid": "berkshire-hathaway"
          },
          {
            "symbol": "NYSE:NEM",
            "logoid": "newmont"
          },
          {
            "symbol": "NYSE:ABBV",
            "logoid": "abbvie"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "TSX:ABX",
            "logoid": "barrick-gold"
          },
          {
            "symbol": "AMEX:XLF",
            "logoid": "sector/financial"
          },
          {
            "symbol": "AMEX:XLK",
            "logoid": "sector/technology"
          },
          {
            "symbol": "AMEX:XLB",
            "logoid": "sector/materials"
          },
          {
            "symbol": "AMEX:XLV",
            "logoid": "sector/health-care"
          },
          {
            "symbol": "NASDAQ:LIN",
            "logoid": "linde"
          }
        ],
        "storyPath": "/news/zacks:814268de4094b:0-top-ranked-etfs-to-power-your-portfolio-higher/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:6e2fdbdca094b:0",
        "title": "Capturing AI Gains Without Overexposure: ETFs to Consider",
        "published": 1764946920,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2800353/capturing-ai-gains-without-overexposure-etfs-to-consider?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2800353",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:QQQ",
            "logoid": "invesco"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "AMEX:SPY",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "AMEX:VOO",
            "logoid": "vanguard"
          },
          {
            "symbol": "AMEX:IVV",
            "logoid": "ishares"
          },
          {
            "symbol": "AMEX:XNTK",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "AMEX:RSPT",
            "logoid": "invesco"
          },
          {
            "symbol": "AMEX:SPYM",
            "logoid": "spdr-sandp500-etf-tr"
          }
        ],
        "storyPath": "/news/zacks:6e2fdbdca094b:0-capturing-ai-gains-without-overexposure-etfs-to-consider/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:c16d0e9c5094b:0",
        "title": "Mag 7 Beats S&P 500 in Q3: Buy These 3 ETFs to Tap Their Strength",
        "published": 1764784080,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2799157/mag-7-beats-s-p-500-in-q3-buy-these-3-etfs-to-tap-their-strength?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2799157",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "AMEX:IYW",
            "logoid": "ishares"
          },
          {
            "symbol": "AMEX:XLG",
            "logoid": "invesco"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:QQMG",
            "logoid": "invesco"
          }
        ],
        "storyPath": "/news/zacks:c16d0e9c5094b:0-mag-7-beats-s-p-500-in-q3-buy-these-3-etfs-to-tap-their-strength/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "leverage_shares:8c582a64b094b:0",
        "title": "Apple Q4 Earnings: Services and AI Drive a Structural Turnaround",
        "published": 1762445206,
        "urgency": 2,
        "link": "https://leverageshares.com/en-eu/insights/apple-q4-earnings-services-and-ai-drive-a-structural-turnaround/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/leverage_shares:8c582a64b094b:0-apple-q4-earnings-services-and-ai-drive-a-structural-turnaround/",
        "provider": {
          "id": "leverage_shares",
          "name": "Leverage Shares",
          "logo_id": "leverage-shares",
          "url": "https://leverageshares.com/en/"
        }
      },
      {
        "id": "zacks:f59de06ac094b:0",
        "title": "With Strong Holiday Outlook for iPhones, Can Apple ETFs Gain Ahead? ",
        "published": 1762344000,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2785373/with-strong-holiday-outlook-for-iphones-can-apple-etfs-gain-ahead?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2785373",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/zacks:f59de06ac094b:0-with-strong-holiday-outlook-for-iphones-can-apple-etfs-gain-ahead/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:bf6faad7c094b:0",
        "title": "Best-Performing ETFs of Last Week",
        "published": 1762169580,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2783196/best-performing-etfs-of-last-week?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2783196",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "TVC:DJI",
            "logoid": "indices/dow-30"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/zacks:bf6faad7c094b:0-best-performing-etfs-of-last-week/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:b27e47d19094b:0",
        "title": "Mag-7 Earnings: Trick or Treat for ETF Investors?",
        "published": 1761915600,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2782438/mag-7-earnings-trick-or-treat-for-etf-investors?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2782438",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/zacks:b27e47d19094b:0-mag-7-earnings-trick-or-treat-for-etf-investors/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L4N3WC0EE:0",
        "title": "US equity fund inflows eased before Fed decision and big tech earnings",
        "published": 1761913361,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L4N3WC0EE:0-us-equity-fund-inflows-eased-before-fed-decision-and-big-tech-earnings/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "zacks:9d6ef00ee094b:0",
        "title": "What Lies Ahead for Mag-7 ETFs in Q3 Earnings Season?",
        "published": 1761214980,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2774835/what-lies-ahead-for-mag-7-etfs-in-q3-earnings-season?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2774835",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "AMEX:XLG",
            "logoid": "invesco"
          },
          {
            "symbol": "AMEX:MGK",
            "logoid": "vanguard"
          },
          {
            "symbol": "TSX:BMO",
            "logoid": "bank-of-montreal"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          }
        ],
        "storyPath": "/news/zacks:9d6ef00ee094b:0-what-lies-ahead-for-mag-7-etfs-in-q3-earnings-season/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:fb1f7d4ce094b:0",
        "title": "What's Driving the Surge in Rare Earth Stocks",
        "published": 1761077340,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2773486/what-s-driving-the-surge-in-rare-earth-stocks?cid=CS-TRADINGVIEW-FT-etf_spotlight-2773486",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:MP",
            "logoid": "mp-materials"
          }
        ],
        "storyPath": "/news/zacks:fb1f7d4ce094b:0-what-s-driving-the-surge-in-rare-earth-stocks/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:4884dc0e4094b:0",
        "title": "Apple at All-Time High on iPhone 17 Boom: ETFs to Consider",
        "published": 1761058380,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2773258/apple-at-all-time-high-on-iphone-17-boom-etfs-to-consider?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2773258",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/zacks:4884dc0e4094b:0-apple-at-all-time-high-on-iphone-17-boom-etfs-to-consider/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:604c6030b094b:0",
        "title": "U.S.-China Trade Tensions Stiffen: ETF Areas Likely to Lose the Most",
        "published": 1760349600,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2767109/u-s-china-trade-tensions-stiffen-etf-areas-likely-to-lose-the-most?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2767109",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMD",
            "logoid": "advanced-micro-devices"
          },
          {
            "symbol": "NASDAQ:QCOM",
            "logoid": "qualcomm"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/zacks:604c6030b094b:0-u-s-china-trade-tensions-stiffen-etf-areas-likely-to-lose-the-most/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:3214a878b094b:0",
        "title": "Best-Performing ETF Areas of September",
        "published": 1759316400,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2760019/best-performing-etf-areas-of-september?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2760019",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:INTC",
            "logoid": "intel"
          }
        ],
        "storyPath": "/news/zacks:3214a878b094b:0-best-performing-etf-areas-of-september/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:eb2d8746e094b:0",
        "title": "Fed Signals More Easing: Can S&P 500 ETFs Rally Further?",
        "published": 1758621600,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2755413/fed-signals-more-easing-can-s-p-500-etfs-rally-further?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2755413",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "BCBA:SPY",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "LSE:BARC",
            "logoid": "barclays"
          },
          {
            "symbol": "NYSE:GS",
            "logoid": "golden-sachs-etf-trust-goldman"
          },
          {
            "symbol": "NYSE:WFC",
            "logoid": "wells-fargo"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          }
        ],
        "storyPath": "/news/zacks:eb2d8746e094b:0-fed-signals-more-easing-can-s-p-500-etfs-rally-further/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:911963a8c094b:0",
        "title": "Boost Your Portfolio With These Top-Ranked ETFs",
        "published": 1758297780,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2754255/boost-your-portfolio-with-these-top-ranked-etfs?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2754255",
        "relatedSymbols": [
          {
            "symbol": "NYSE:JPM",
            "logoid": "jpmorgan-chase"
          },
          {
            "symbol": "NYSE:CAT",
            "logoid": "caterpillar"
          },
          {
            "symbol": "NYSE:JNJ",
            "logoid": "johnson-and-johnson"
          },
          {
            "symbol": "NYSE:LLY",
            "logoid": "eli-lilly"
          },
          {
            "symbol": "NYSE:BRK.A",
            "logoid": "berkshire-hathaway"
          },
          {
            "symbol": "NYSE:ABBV",
            "logoid": "abbvie"
          },
          {
            "symbol": "NYSE:RTX",
            "logoid": "raytheon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "TSX:ABX",
            "logoid": "barrick-gold"
          },
          {
            "symbol": "AMEX:XLF",
            "logoid": "sector/financial"
          },
          {
            "symbol": "AMEX:XLK",
            "logoid": "sector/technology"
          },
          {
            "symbol": "AMEX:XLI",
            "logoid": "sector/industrial"
          },
          {
            "symbol": "AMEX:XLV",
            "logoid": "sector/health-care"
          }
        ],
        "storyPath": "/news/zacks:911963a8c094b:0-boost-your-portfolio-with-these-top-ranked-etfs/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:5dee8aed8094b:0",
        "title": "Pain or Gain Ahead of Apple? ETFs in Focus ",
        "published": 1758022380,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2751953/pain-or-gain-ahead-of-apple-etfs-in-focus?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2751953",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/zacks:5dee8aed8094b:0-pain-or-gain-ahead-of-apple-etfs-in-focus/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:e630369f0094b:0",
        "title": "Analysts Boost S&P 500 Target: ETFs in Focus ",
        "published": 1757930400,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2751203/analysts-boost-s-p-500-target-etfs-in-focus?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2751203",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "BCBA:SPY",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/zacks:e630369f0094b:0-analysts-boost-s-p-500-target-etfs-in-focus/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:c237dd468094b:0",
        "title": "Apple Falls After iPhone 17 Launch: What Lies Ahead for ETFs?",
        "published": 1757503560,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2749177/apple-falls-after-iphone-17-launch-what-lies-ahead-for-etfs?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2749177",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/zacks:c237dd468094b:0-apple-falls-after-iphone-17-launch-what-lies-ahead-for-etfs/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:e5cbc15e2094b:0",
        "title": "Should You Bet on Apple-Heavy ETFs Now?",
        "published": 1757005560,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2747330/should-you-bet-on-apple-heavy-etfs-now?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2747330",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/zacks:e5cbc15e2094b:0-should-you-bet-on-apple-heavy-etfs-now/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:4bdb9c4f6094b:0",
        "title": "4 Factors That Could Boost S&P 500 Even Further in 2026",
        "published": 1756983600,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2747031/4-factors-that-could-boost-s-p-500-even-further-in-2026?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2747031",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/zacks:4bdb9c4f6094b:0-4-factors-that-could-boost-s-p-500-even-further-in-2026/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L1N3UQ0Q8:0",
        "title": "Mexico's Grupo BMV plans to launch options for major US stocks like Amazon",
        "published": 1756980000,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "BMV:BOLSA/A",
            "logoid": "bolsa-mexicana-de-valores-sab-de-cv"
          },
          {
            "symbol": "NYSE:TBBB",
            "logoid": "bbb-foods-inc"
          },
          {
            "symbol": "NASDAQ:CME",
            "logoid": "cme"
          }
        ],
        "isExclusive": true,
        "storyPath": "/news/reuters.com,2025:newsml_L1N3UQ0Q8:0-mexico-s-grupo-bmv-plans-to-launch-options-for-major-us-stocks-like-amazon/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "zacks:ea098fee7094b:0",
        "title": "Apple-Google Likely Tie-Up for Siri Revamp Puts These ETFs in Focus ",
        "published": 1756202400,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2742630/apple-google-likely-tie-up-for-siri-revamp-puts-these-etfs-in-focus?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2742630",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          }
        ],
        "storyPath": "/news/zacks:ea098fee7094b:0-apple-google-likely-tie-up-for-siri-revamp-puts-these-etfs-in-focus/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:757ce3f5c094b:0",
        "title": "AI Fatigue Hits Tech Biggies: Inverse ETFs in Focus ",
        "published": 1755772200,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2740586/ai-fatigue-hits-tech-biggies-inverse-etfs-in-focus?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2740586",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:CRWV",
            "logoid": "coreweave"
          },
          {
            "symbol": "NASDAQ:PLTR",
            "logoid": "palantir"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          }
        ],
        "storyPath": "/news/zacks:757ce3f5c094b:0-ai-fatigue-hits-tech-biggies-inverse-etfs-in-focus/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:4de13fa89094b:0",
        "title": "Bridgewater Shies Away From China: Time for Inverse China ETFs?",
        "published": 1755685920,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2739190/bridgewater-shies-away-from-china-time-for-inverse-china-etfs?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2739190",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:4de13fa89094b:0-bridgewater-shies-away-from-china-time-for-inverse-china-etfs/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:0c767b982094b:0",
        "title": "Invest Like Warren Buffett With These ETFs",
        "published": 1755513900,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2729238/invest-like-warren-buffett-with-these-etfs?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2729238",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:UNH",
            "logoid": "unitedhealth"
          },
          {
            "symbol": "NYSE:BRK.A",
            "logoid": "berkshire-hathaway"
          },
          {
            "symbol": "NYSE:BAC",
            "logoid": "bank-of-america"
          }
        ],
        "storyPath": "/news/zacks:0c767b982094b:0-invest-like-warren-buffett-with-these-etfs/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L4N3U70CC:0",
        "title": "US equity funds draw weekly inflows on rate cut hopes",
        "published": 1755256783,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L4N3U70CC:0-us-equity-funds-draw-weekly-inflows-on-rate-cut-hopes/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L4N3U70CD:0",
        "title": "Global equity fund inflows at six-week high on soft US inflation, tariff truce",
        "published": 1755250515,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L4N3U70CD:0-global-equity-fund-inflows-at-six-week-high-on-soft-us-inflation-tariff-truce/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "zacks:e7e8f5802094b:0",
        "title": "S&P 500 Hits 6,400 on AI Boom: ETFs in Focus",
        "published": 1755168180,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2711351/s-p-500-hits-6-400-on-ai-boom-etfs-in-focus?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2711351",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:AVGO",
            "logoid": "broadcom"
          },
          {
            "symbol": "NASDAQ:PLTR",
            "logoid": "palantir"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:NFLX",
            "logoid": "netflix"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:ORCL",
            "logoid": "oracle"
          },
          {
            "symbol": "NYSE:JPM",
            "logoid": "jpmorgan-chase"
          }
        ],
        "storyPath": "/news/zacks:e7e8f5802094b:0-s-p-500-hits-6-400-on-ai-boom-etfs-in-focus/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:ca46661d2094b:0",
        "title": "S&P 500 ETFs Hit Record Highs as Index Tops 6,400: What's Next?",
        "published": 1755095400,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2707453/s-p-500-etfs-hit-record-highs-as-index-tops-6-400-what-s-next?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2707453",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "AMEX:SPY",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "AMEX:VOO",
            "logoid": "vanguard"
          },
          {
            "symbol": "AMEX:IVV",
            "logoid": "ishares"
          }
        ],
        "storyPath": "/news/zacks:ca46661d2094b:0-s-p-500-etfs-hit-record-highs-as-index-tops-6-400-what-s-next/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:eba9fe36f094b:0",
        "title": "5 Most-Loved ETFs of Last Week",
        "published": 1755007200,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2702347/5-most-loved-etfs-of-last-week?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2702347",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:VCSH",
            "logoid": "vanguard"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "AMEX:VOO",
            "logoid": "vanguard"
          },
          {
            "symbol": "AMEX:IVV",
            "logoid": "ishares"
          },
          {
            "symbol": "AMEX:XLC",
            "logoid": "communication-services"
          },
          {
            "symbol": "AMEX:SGOV"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          }
        ],
        "storyPath": "/news/zacks:eba9fe36f094b:0-5-most-loved-etfs-of-last-week/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "leverage_shares:a57b0183d094b:0",
        "title": "Apple Q3 Earnings Trends: Unfazed by Tariffs?",
        "published": 1754982000,
        "urgency": 2,
        "link": "https://leverageshares.com/en-eu/insights/apple-q3-earnings-trends-unfazed-by-tariffs/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/leverage_shares:a57b0183d094b:0-apple-q3-earnings-trends-unfazed-by-tariffs/",
        "provider": {
          "id": "leverage_shares",
          "name": "Leverage Shares",
          "logo_id": "leverage-shares",
          "url": "https://leverageshares.com/en/"
        }
      },
      {
        "id": "zacks:25e7ea37d094b:0",
        "title": "Technology ETF (XNTK) Hits New 52-Week High",
        "published": 1754925300,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2697730/technology-etf-xntk-hits-new-52-week-high?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2697730",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "AMEX:XNTK",
            "logoid": "spdr-sandp500-etf-tr"
          }
        ],
        "storyPath": "/news/zacks:25e7ea37d094b:0-technology-etf-xntk-hits-new-52-week-high/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:dea9cc37b094b:0",
        "title": "3 Reasons Why Nasdaq ETFs Hit a Record High ",
        "published": 1754649300,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2683172/3-reasons-why-nasdaq-etfs-hit-a-record-high?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2683172",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMD",
            "logoid": "advanced-micro-devices"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:dea9cc37b094b:0-3-reasons-why-nasdaq-etfs-hit-a-record-high/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:000bdc41f094b:0",
        "title": "ETFs Set to Benefit from Apple's $100B U.S. Bet ",
        "published": 1754580600,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2679247/etfs-set-to-benefit-from-apple-s-100b-u-s-bet?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2679247",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/zacks:000bdc41f094b:0-etfs-set-to-benefit-from-apple-s-100b-u-s-bet/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:0e45dab69094b:0",
        "title": "ETF Asset Report of the Month of July ",
        "published": 1754389680,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2666570/etf-asset-report-of-the-month-of-july?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2666570",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "AMEX:IWM",
            "logoid": "ishares"
          },
          {
            "symbol": "BCBA:SPY",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          }
        ],
        "storyPath": "/news/zacks:0e45dab69094b:0-etf-asset-report-of-the-month-of-july/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:3fea917ee094b:0",
        "title": "Take a Bite of Apple's Solid Q3 Earnings With These ETFs",
        "published": 1754056800,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2649303/take-a-bite-of-apple-s-solid-q3-earnings-with-these-etfs?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2649303",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/zacks:3fea917ee094b:0-take-a-bite-of-apple-s-solid-q3-earnings-with-these-etfs/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:799bc5b7d094b:0",
        "title": "Nasdaq Covered Call ETFs for Growth & Income",
        "published": 1753984560,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2645075/nasdaq-covered-call-etfs-for-growth-income?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2645075",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:QYLD",
            "logoid": "global-x"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "AMEX:JEPI",
            "logoid": "jpmorgan"
          },
          {
            "symbol": "NASDAQ:JEPQ",
            "logoid": "jpmorgan"
          },
          {
            "symbol": "NASDAQ:QQQI",
            "logoid": "neosfunds"
          },
          {
            "symbol": "AMEX:QDVO",
            "logoid": "amplify"
          },
          {
            "symbol": "NASDAQ:GPIQ",
            "logoid": "golden-sachs-etf-trust-goldman"
          }
        ],
        "storyPath": "/news/zacks:799bc5b7d094b:0-nasdaq-covered-call-etfs-for-growth-income/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:db8f0a7ed094b:0",
        "title": "Single-Stock ETFs in Focus as Big Tech Earnings Unfold",
        "published": 1753797600,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2633724/single-stock-etfs-in-focus-as-big-tech-earnings-unfold?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2633724",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          }
        ],
        "storyPath": "/news/zacks:db8f0a7ed094b:0-single-stock-etfs-in-focus-as-big-tech-earnings-unfold/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:186d21199094b:0",
        "title": "ETFs to Capitalize on TSM's Impressive Q2 Earnings ",
        "published": 1752850800,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2592035/etfs-to-capitalize-on-tsm-s-impressive-q2-earnings?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2592035",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "TWSE:2330",
            "logoid": "taiwan-semiconductor"
          }
        ],
        "storyPath": "/news/zacks:186d21199094b:0-etfs-to-capitalize-on-tsm-s-impressive-q2-earnings/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:c02aade74094b:0",
        "title": "ETFs to Play on AI's Growing Momentum",
        "published": 1752527640,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2580734/etfs-to-play-on-ai-s-growing-momentum?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2580734",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:c02aade74094b:0-etfs-to-play-on-ai-s-growing-momentum/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:f74b7abee094b:0",
        "title": "Tariff-Led Volatility Ahead for Big Tech? ETFs in Focus ",
        "published": 1752494400,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2579332/tariff-led-volatility-ahead-for-big-tech-etfs-in-focus?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2579332",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:f74b7abee094b:0-tariff-led-volatility-ahead-for-big-tech-etfs-in-focus/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:a567ecf2b094b:0",
        "title": "How to Find Attractively Priced Growth Stocks",
        "published": 1751320680,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2558382/how-to-find-attractively-priced-growth-stocks?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2558382",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:a567ecf2b094b:0-how-to-find-attractively-priced-growth-stocks/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:89586e355094b:0",
        "title": "Apple Unveils Big UI Overhaul at WWDC: ETFs in Focus",
        "published": 1749560400,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2492219/apple-unveils-big-ui-overhaul-at-wwdc-etfs-in-focus?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2492219",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/zacks:89586e355094b:0-apple-unveils-big-ui-overhaul-at-wwdc-etfs-in-focus/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:e145ac146094b:0",
        "title": "6 ETFs to Invest in June ",
        "published": 1749229200,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2487851/6-etfs-to-invest-in-june?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2487851",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          }
        ],
        "storyPath": "/news/zacks:e145ac146094b:0-6-etfs-to-invest-in-june/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "leverage_shares:00b057886094b:0",
        "title": "Epic Games Potentially Knocked Out a Key Apple Growth Driver",
        "published": 1749193200,
        "urgency": 2,
        "link": "https://leverageshares.com/en-eu/insights/epic-games-potentially-knocked-out-a-key-apple-growth-driver/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/leverage_shares:00b057886094b:0-epic-games-potentially-knocked-out-a-key-apple-growth-driver/",
        "provider": {
          "id": "leverage_shares",
          "name": "Leverage Shares",
          "logo_id": "leverage-shares",
          "url": "https://leverageshares.com/en/"
        }
      },
      {
        "id": "leverage_shares:23abde207094b:0",
        "title": "Magnificent 7: Earnings Soar, Stocks Lag",
        "published": 1749134541,
        "urgency": 2,
        "link": "https://leverageshares.com/en-eu/insights/magnificent-7-earnings-soar-stocks-lag/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/leverage_shares:23abde207094b:0-magnificent-7-earnings-soar-stocks-lag/",
        "provider": {
          "id": "leverage_shares",
          "name": "Leverage Shares",
          "logo_id": "leverage-shares",
          "url": "https://leverageshares.com/en/"
        }
      },
      {
        "id": "zacks:26134cf02094b:0",
        "title": "Mag 7 ETFs Surge: Will the Rally Keep Rolling?",
        "published": 1749132000,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2485829/mag-7-etfs-surge-will-the-rally-keep-rolling?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2485829",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/zacks:26134cf02094b:0-mag-7-etfs-surge-will-the-rally-keep-rolling/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:34c0aed09094b:0",
        "title": "Why Big Tech Stocks Are Powering Market Gains Again",
        "published": 1749058920,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2484821/why-big-tech-stocks-are-powering-market-gains-again?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2484821",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/zacks:34c0aed09094b:0-why-big-tech-stocks-are-powering-market-gains-again/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "tag:reuters.com,2025-06-04:newsml_NFC91sB1J:0",
        "title": "LongPoint Adds Canada's First Double Leveraged Single Stock ETFs",
        "published": 1749038438,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          }
        ],
        "storyPath": "/news/reuters.com,2025-06-04:newsml_NFC91sB1J:0-longpoint-adds-canada-s-first-double-leveraged-single-stock-etfs/",
        "provider": {
          "id": "newsfilecorp",
          "name": "Newsfile Corp.",
          "logo_id": "rdp-nfc"
        }
      },
      {
        "id": "zacks:3c05c8404094b:0",
        "title": "S&P 500 ETFs Log Best May in 30+ Yrs on AI, Large-Cap Safety",
        "published": 1748970000,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2483740/s-p-500-etfs-log-best-may-in-30-yrs-on-ai-large-cap-safety?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2483740",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "BCBA:SPY",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:3c05c8404094b:0-s-p-500-etfs-log-best-may-in-30-yrs-on-ai-large-cap-safety/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:d47902c7a094b:0",
        "title": "Hot ETFs: Cybersecurity, Income & Bitcoin ",
        "published": 1748457300,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2478520/hot-etfs-cybersecurity-income-bitcoin?cid=CS-TRADINGVIEW-FT-etf_spotlight-2478520",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          }
        ],
        "storyPath": "/news/zacks:d47902c7a094b:0-hot-etfs-cybersecurity-income-bitcoin/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:7d8cfdae1094b:0",
        "title": "Best-Performing ETF Areas of Last Week ",
        "published": 1748365200,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2477875/best-performing-etf-areas-of-last-week?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2477875",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "AMEX:GLD",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "AMEX:PPLT",
            "logoid": "abrdn"
          },
          {
            "symbol": "AMEX:GOEX",
            "logoid": "global-x"
          },
          {
            "symbol": "AMEX:URA",
            "logoid": "global-x"
          },
          {
            "symbol": "AMEX:PLTM",
            "logoid": "graniteshares"
          },
          {
            "symbol": "AMEX:URNM",
            "logoid": "sprott"
          },
          {
            "symbol": "NASDAQ:AUMI",
            "logoid": "themes-gold-miners-etf"
          }
        ],
        "storyPath": "/news/zacks:7d8cfdae1094b:0-best-performing-etf-areas-of-last-week/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:a66667aa7094b:0",
        "title": "Top-Performing Leveraged ETFs of Last Week ",
        "published": 1748347200,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2477513/top-performing-leveraged-etfs-of-last-week?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2477513",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "AMEX:GLD",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "NASDAQ:SMCI",
            "logoid": "super-micro-computer"
          },
          {
            "symbol": "AMEX:GDX",
            "logoid": "vaneck"
          },
          {
            "symbol": "TSX:BMO",
            "logoid": "bank-of-montreal"
          },
          {
            "symbol": "NYSE:IONQ",
            "logoid": "ionq"
          },
          {
            "symbol": "NASDAQ:RGTI",
            "logoid": "rigetti-computing-redeemable"
          },
          {
            "symbol": "NASDAQ:IONX",
            "logoid": "differential-series-solutions"
          },
          {
            "symbol": "NASDAQ:SMCZ",
            "logoid": "differential-series-solutions"
          },
          {
            "symbol": "NASDAQ:RGTX",
            "logoid": "differential-series-solutions"
          }
        ],
        "storyPath": "/news/zacks:a66667aa7094b:0-top-performing-leveraged-etfs-of-last-week/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:a65b883da094b:0",
        "title": "Volatility ETFs Spike on Renewed Trump Tariff Threats",
        "published": 1748268000,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2477225/volatility-etfs-spike-on-renewed-trump-tariff-threats?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2477225",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/zacks:a65b883da094b:0-volatility-etfs-spike-on-renewed-trump-tariff-threats/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:518920b92094b:0",
        "title": "Tap Mag-7 ETFs on Temporary US-China Trade Truce",
        "published": 1747133160,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2467547/tap-mag-7-etfs-on-temporary-us-china-trade-truce?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2467547",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "BCBA:SPY",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/zacks:518920b92094b:0-tap-mag-7-etfs-on-temporary-us-china-trade-truce/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:afd8679c8094b:0",
        "title": "ETFs on the Move Post U.S.-China Trade Deal",
        "published": 1747068720,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2467079/etfs-on-the-move-post-u-s-china-trade-deal?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2467079",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          }
        ],
        "storyPath": "/news/zacks:afd8679c8094b:0-etfs-on-the-move-post-u-s-china-trade-deal/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:c2aaba522094b:0",
        "title": "3 ETF Strategies to Follow on Temporary U.S.-China Trade Deal",
        "published": 1747047180,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2466519/3-etf-strategies-to-follow-on-temporary-u-s-china-trade-deal?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2466519",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NYSE:BABA",
            "logoid": "alibaba"
          },
          {
            "symbol": "NASDAQ:JD",
            "logoid": "jd-com"
          },
          {
            "symbol": "TWSE:2330",
            "logoid": "taiwan-semiconductor"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:BIDU",
            "logoid": "baidu"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:c2aaba522094b:0-3-etf-strategies-to-follow-on-temporary-u-s-china-trade-deal/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:2aac4dcb0094b:0",
        "title": "Tech ETFs at the Forefront of the Current Market Rally",
        "published": 1746800940,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2466165/tech-etfs-at-the-forefront-of-the-current-market-rally?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2466165",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          }
        ],
        "storyPath": "/news/zacks:2aac4dcb0094b:0-tech-etfs-at-the-forefront-of-the-current-market-rally/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:a66c1ab70094b:0",
        "title": "5 Top-Ranked ETFs That Have Outperformed S&P 500 Since April Low",
        "published": 1746716400,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2465319/5-top-ranked-etfs-that-have-outperformed-s-p-500-since-april-low?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2465319",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          }
        ],
        "storyPath": "/news/zacks:a66c1ab70094b:0-5-top-ranked-etfs-that-have-outperformed-s-p-500-since-april-low/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:15fef8583094b:0",
        "title": "Don't Sell in May and Go Away: Follow These ETF Strategies",
        "published": 1746554700,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2463365/don-t-sell-in-may-and-go-away-follow-these-etf-strategies?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2463365",
        "relatedSymbols": [
          {
            "symbol": "AMEX:XLP",
            "logoid": "sector/consumer-staples"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          }
        ],
        "storyPath": "/news/zacks:15fef8583094b:0-don-t-sell-in-may-and-go-away-follow-these-etf-strategies/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:6a02ae310094b:0",
        "title": "Why Big Tech ETFs Still Remain Great Bets",
        "published": 1746535320,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2462813/why-big-tech-etfs-still-remain-great-bets?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2462813",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:QQQ",
            "logoid": "invesco"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          }
        ],
        "storyPath": "/news/zacks:6a02ae310094b:0-why-big-tech-etfs-still-remain-great-bets/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:f42f5c1ca094b:0",
        "title": "Inside Last Week's Wall Street Rally & Best-Performing ETF Areas ",
        "published": 1746524940,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2462639/inside-last-week-s-wall-street-rally-best-performing-etf-areas?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2462639",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          }
        ],
        "storyPath": "/news/zacks:f42f5c1ca094b:0-inside-last-week-s-wall-street-rally-best-performing-etf-areas/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:cdd4a2517094b:0",
        "title": "Here's How to Invest in ETFs With Warren Buffett's Strategies",
        "published": 1746460800,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2462316/here-s-how-to-invest-in-etfs-with-warren-buffett-s-strategies?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2462316",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:KO",
            "logoid": "coca-cola"
          },
          {
            "symbol": "NYSE:BRK.A",
            "logoid": "berkshire-hathaway"
          },
          {
            "symbol": "NYSE:AXP",
            "logoid": "american-express"
          }
        ],
        "storyPath": "/news/zacks:cdd4a2517094b:0-here-s-how-to-invest-in-etfs-with-warren-buffett-s-strategies/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:bd6a51874094b:0",
        "title": "Forget 'Sell in May': 5 Factors Why Wall Street ETFs Could Rally Ahead",
        "published": 1746435060,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2461627/forget-sell-in-may-5-factors-why-wall-street-etfs-could-rally-ahead?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2461627",
        "relatedSymbols": [
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "TVC:DJI",
            "logoid": "indices/dow-30"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          }
        ],
        "storyPath": "/news/zacks:bd6a51874094b:0-forget-sell-in-may-5-factors-why-wall-street-etfs-could-rally-ahead/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:67d272df0094b:0",
        "title": "Can S&P 500 ETFs Continue Their Winning Streak?",
        "published": 1746201600,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2461439/can-s-p-500-etfs-continue-their-winning-streak?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2461439",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          }
        ],
        "storyPath": "/news/zacks:67d272df0094b:0-can-s-p-500-etfs-continue-their-winning-streak/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:d63e2f487094b:0",
        "title": "Apple Beats on Q2 Earnings but Shares Slip: ETFs to Watch",
        "published": 1746195060,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2461298/apple-beats-on-q2-earnings-but-shares-slip-etfs-to-watch?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2461298",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/zacks:d63e2f487094b:0-apple-beats-on-q2-earnings-but-shares-slip-etfs-to-watch/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:912e76d6d094b:0",
        "title": "Apple ETFs in Focus Ahead of Fiscal Q2 Earnings",
        "published": 1746029700,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2459317/apple-etfs-in-focus-ahead-of-fiscal-q2-earnings?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2459317",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/zacks:912e76d6d094b:0-apple-etfs-in-focus-ahead-of-fiscal-q2-earnings/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:1eaaeb8a7094b:0",
        "title": "S&P 500 on a Winning Streak Since November: VOO vs. SPY ETF",
        "published": 1746026100,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2459201/s-p-500-on-a-winning-streak-since-november-voo-vs-spy-etf?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2459201",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "AMEX:SPY",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "AMEX:VOO",
            "logoid": "vanguard"
          },
          {
            "symbol": "AMEX:IVV",
            "logoid": "ishares"
          }
        ],
        "storyPath": "/news/zacks:1eaaeb8a7094b:0-s-p-500-on-a-winning-streak-since-november-voo-vs-spy-etf/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:2f1b91dfd094b:0",
        "title": "A Glimpse at Trump's 100 Days in Office: ETF Winners & Losers",
        "published": 1746019800,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2458881/a-glimpse-at-trump-s-100-days-in-office-etf-winners-losers?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2458881",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "TVC:DJI",
            "logoid": "indices/dow-30"
          }
        ],
        "storyPath": "/news/zacks:2f1b91dfd094b:0-a-glimpse-at-trump-s-100-days-in-office-etf-winners-losers/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:2a197f604094b:0",
        "title": "Can Q1 Earnings Inject Fresh Life Into Magnificent 7 ETFs?",
        "published": 1745847000,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2456740/can-q1-earnings-inject-fresh-life-into-magnificent-7-etfs?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2456740",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          }
        ],
        "storyPath": "/news/zacks:2a197f604094b:0-can-q1-earnings-inject-fresh-life-into-magnificent-7-etfs/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:102538e05094b:0",
        "title": "Tariff Relief Talks Lift Tech ETFs, Stocks: What's Ahead?",
        "published": 1745505900,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2455057/tariff-relief-talks-lift-tech-etfs-stocks-what-s-ahead?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2455057",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          }
        ],
        "storyPath": "/news/zacks:102538e05094b:0-tariff-relief-talks-lift-tech-etfs-stocks-what-s-ahead/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:a43ad7179094b:0",
        "title": "Are Apple ETFs Ripe for a Rebound?",
        "published": 1745427600,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2454024/are-apple-etfs-ripe-for-a-rebound?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2454024",
        "relatedSymbols": [
          {
            "symbol": "BCBA:SPY",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:QQQ",
            "logoid": "invesco"
          }
        ],
        "storyPath": "/news/zacks:a43ad7179094b:0-are-apple-etfs-ripe-for-a-rebound/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:bf0a94566094b:0",
        "title": "Should You Brace for Mag-7 ETFs Before It's Too Late?",
        "published": 1744736400,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2449382/should-you-brace-for-mag-7-etfs-before-it-s-too-late?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2449382",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          }
        ],
        "storyPath": "/news/zacks:bf0a94566094b:0-should-you-brace-for-mag-7-etfs-before-it-s-too-late/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L4N3QQ01D:0",
        "title": "Bullish trade in Apple options reaps gains as shares jump on tariff exemption",
        "published": 1744641917,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "AMEX:SPY",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NDX",
            "logoid": "indices/nasdaq-100"
          },
          {
            "symbol": "CBOE:SPX",
            "logoid": "indices/s-and-p-500"
          },
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L4N3QQ01D:0-bullish-trade-in-apple-options-reaps-gains-as-shares-jump-on-tariff-exemption/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "zacks:b442a1856094b:0",
        "title": "Tech Set to Surge on Tariff Pause: 5 ETF Picks",
        "published": 1744639200,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2448473/tech-set-to-surge-on-tariff-pause-5-etf-picks?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2448473",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          }
        ],
        "storyPath": "/news/zacks:b442a1856094b:0-tech-set-to-surge-on-tariff-pause-5-etf-picks/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:fbf9a3d4b094b:0",
        "title": "Rally in Apple ETFs in the Cards?",
        "published": 1744634280,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2448244/rally-in-apple-etfs-in-the-cards?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2448244",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/zacks:fbf9a3d4b094b:0-rally-in-apple-etfs-in-the-cards/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:a66975d5b094b:0",
        "title": "US-Sino Trade War Escalates: ETF Areas Under Pressure ",
        "published": 1744390800,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2447960/us-sino-trade-war-escalates-etf-areas-under-pressure?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2447960",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:QCOM",
            "logoid": "qualcomm"
          },
          {
            "symbol": "NYSE:MGM",
            "logoid": "mgm-resorts"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:WYNN",
            "logoid": "wynn-resorts"
          }
        ],
        "storyPath": "/news/zacks:a66975d5b094b:0-us-sino-trade-war-escalates-etf-areas-under-pressure/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:0898505e3094b:0",
        "title": "Apple Stock Suffers Sharp Selloff: Buy the Dip in ETFs?",
        "published": 1744135200,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2442182/apple-stock-suffers-sharp-selloff-buy-the-dip-in-etfs?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2442182",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/zacks:0898505e3094b:0-apple-stock-suffers-sharp-selloff-buy-the-dip-in-etfs/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:4d4291c3a094b:0",
        "title": "3 Tech ETFs on Sale Now ",
        "published": 1744115940,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2441713/3-tech-etfs-on-sale-now?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2441713",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:AVGO",
            "logoid": "broadcom"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NDAQ",
            "logoid": "nasdaq"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          }
        ],
        "storyPath": "/news/zacks:4d4291c3a094b:0-3-tech-etfs-on-sale-now/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:e8f2a6d4e094b:0",
        "title": "Nasdaq in Bear Market: Buy the Dip in ETFs?",
        "published": 1744045200,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2441433/nasdaq-in-bear-market-buy-the-dip-in-etfs?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2441433",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          }
        ],
        "storyPath": "/news/zacks:e8f2a6d4e094b:0-nasdaq-in-bear-market-buy-the-dip-in-etfs/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:f6b6fd582094b:0",
        "title": "5 ETFs Withstanding the Biggest Market Drop Since 2020",
        "published": 1743779700,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2440641/5-etfs-withstanding-the-biggest-market-drop-since-2020?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2440641",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          }
        ],
        "storyPath": "/news/zacks:f6b6fd582094b:0-5-etfs-withstanding-the-biggest-market-drop-since-2020/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:57297b9e8094b:0",
        "title": "Inside Trump Tariffs and Their Impact on Sector ETFs",
        "published": 1743699600,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2440014/inside-trump-tariffs-and-their-impact-on-sector-etfs?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2440014",
        "relatedSymbols": [
          {
            "symbol": "AMEX:XRT",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:GM",
            "logoid": "general-motors"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          }
        ],
        "storyPath": "/news/zacks:57297b9e8094b:0-inside-trump-tariffs-and-their-impact-on-sector-etfs/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:56a837a1e094b:0",
        "title": "Can the Tide Turn for 'Magnificent Seven' Stocks? ETFs in Focus",
        "published": 1743076800,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2436001/can-the-tide-turn-for-magnificent-seven-stocks-etfs-in-focus?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2436001",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          }
        ],
        "storyPath": "/news/zacks:56a837a1e094b:0-can-the-tide-turn-for-magnificent-seven-stocks-etfs-in-focus/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:1f46b704c094b:0",
        "title": "5 Beaten-Down ETFs to Buy Now",
        "published": 1741615200,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2427768/5-beaten-down-etfs-to-buy-now?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2427768",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:PTF",
            "logoid": "invesco"
          },
          {
            "symbol": "NASDAQ:AIRR",
            "logoid": "first-trust"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NFLX",
            "logoid": "netflix"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "AMEX:IWP",
            "logoid": "ishares"
          },
          {
            "symbol": "AMEX:RPG",
            "logoid": "invesco"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:DAT"
          }
        ],
        "storyPath": "/news/zacks:1f46b704c094b:0-5-beaten-down-etfs-to-buy-now/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:6a813e4d4094b:0",
        "title": "4 Reasons to Buy the Dip in Nasdaq ETFs",
        "published": 1741354080,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2427144/4-reasons-to-buy-the-dip-in-nasdaq-etfs?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2427144",
        "relatedSymbols": [
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "HKEX:700",
            "logoid": "tencent"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NYSE:BABA",
            "logoid": "alibaba"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          }
        ],
        "storyPath": "/news/zacks:6a813e4d4094b:0-4-reasons-to-buy-the-dip-in-nasdaq-etfs/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:281529834094b:0",
        "title": "Is This the Perfect Time to Invest in Uranium ETFs?",
        "published": 1740679800,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2423160/is-this-the-perfect-time-to-invest-in-uranium-etfs?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2423160",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "AMEX:URA",
            "logoid": "global-x"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          }
        ],
        "storyPath": "/news/zacks:281529834094b:0-is-this-the-perfect-time-to-invest-in-uranium-etfs/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:c175feaf6094b:0",
        "title": "ETF Strategies to Follow From Buffett's Defensive Stance ",
        "published": 1740421800,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2420588/etf-strategies-to-follow-from-buffett-s-defensive-stance?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2420588",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:BRK.A",
            "logoid": "berkshire-hathaway"
          },
          {
            "symbol": "NYSE:BAC",
            "logoid": "bank-of-america"
          }
        ],
        "storyPath": "/news/zacks:c175feaf6094b:0-etf-strategies-to-follow-from-buffett-s-defensive-stance/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:afc37ad68094b:0",
        "title": "Best-Performing Leveraged ETFs of Last Week",
        "published": 1739883600,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2417299/best-performing-leveraged-etfs-of-last-week?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2417299",
        "relatedSymbols": [
          {
            "symbol": "NYSE:BABA",
            "logoid": "alibaba"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:SMCI",
            "logoid": "super-micro-computer"
          }
        ],
        "storyPath": "/news/zacks:afc37ad68094b:0-best-performing-leveraged-etfs-of-last-week/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:535e0948e094b:0",
        "title": "Is Meta Now the Lone Star in the Big Tech Cohort? ETFs in Focus ",
        "published": 1739556000,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2416446/is-meta-now-the-lone-star-in-the-big-tech-cohort-etfs-in-focus?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2416446",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          }
        ],
        "storyPath": "/news/zacks:535e0948e094b:0-is-meta-now-the-lone-star-in-the-big-tech-cohort-etfs-in-focus/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:df8fb983b094b:0",
        "title": "Should WisdomTree U.S. LargeCap Dividend ETF (DLN) Be on Your Investing Radar?",
        "published": 1739272807,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2413320/should-wisdomtree-u-s-largecap-dividend-etf-dln-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2413320",
        "relatedSymbols": [
          {
            "symbol": "NYSE:JPM",
            "logoid": "jpmorgan-chase"
          },
          {
            "symbol": "AMEX:DLN",
            "logoid": "wisdomtree"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "AMEX:VTV",
            "logoid": "vanguard"
          },
          {
            "symbol": "AMEX:SCHD",
            "logoid": "schwab"
          }
        ],
        "storyPath": "/news/zacks:df8fb983b094b:0-should-wisdomtree-u-s-largecap-dividend-etf-dln-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:c2619839d094b:0",
        "title": "Trump's Tariffs and Their Impact on Auto ETFs",
        "published": 1738951200,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2412251/trump-s-tariffs-and-their-impact-on-auto-etfs?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2412251",
        "relatedSymbols": [
          {
            "symbol": "NYSE:GM",
            "logoid": "general-motors"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:F",
            "logoid": "ford"
          }
        ],
        "storyPath": "/news/zacks:c2619839d094b:0-trump-s-tariffs-and-their-impact-on-auto-etfs/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:7b3154a62094b:0",
        "title": "Is First Trust Dow 30 Equal Weight ETF (EDOW) a Strong ETF Right Now?",
        "published": 1738927204,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2411744/is-first-trust-dow-30-equal-weight-etf-edow-a-strong-etf-right-now?cid=CS-TRADINGVIEW-FT-smart_beta_etf-2411744",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:BA",
            "logoid": "boeing"
          },
          {
            "symbol": "NASDAQ:CSCO",
            "logoid": "cisco"
          },
          {
            "symbol": "BCBA:SPY",
            "logoid": "spdr-sandp500-etf-tr"
          }
        ],
        "storyPath": "/news/zacks:7b3154a62094b:0-is-first-trust-dow-30-equal-weight-etf-edow-a-strong-etf-right-now/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:c1d4e9874094b:0",
        "title": "Is WisdomTree U.S. LargeCap Dividend ETF (DLN) a Strong ETF Right Now?",
        "published": 1738927203,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2411745/is-wisdomtree-u-s-largecap-dividend-etf-dln-a-strong-etf-right-now?cid=CS-TRADINGVIEW-FT-smart_beta_etf-2411745",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          }
        ],
        "storyPath": "/news/zacks:c1d4e9874094b:0-is-wisdomtree-u-s-largecap-dividend-etf-dln-a-strong-etf-right-now/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:f4f6ef5da094b:0",
        "title": "Should Invesco NASDAQ 100 ETF (QQQM) Be on Your Investing Radar?",
        "published": 1738840808,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2410696/should-invesco-nasdaq-100-etf-qqqm-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2410696",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:f4f6ef5da094b:0-should-invesco-nasdaq-100-etf-qqqm-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:d918d40f8094b:0",
        "title": "Should You Invest in the Vanguard Information Technology ETF (VGT)?",
        "published": 1738840808,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2410698/should-you-invest-in-the-vanguard-information-technology-etf-vgt?cid=CS-TRADINGVIEW-FT-sector_etf-2410698",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:d918d40f8094b:0-should-you-invest-in-the-vanguard-information-technology-etf-vgt/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:af7bca24e094b:0",
        "title": "Should iShares S&P 500 Growth ETF (IVW) Be on Your Investing Radar?",
        "published": 1738840807,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2410702/should-ishares-s-p-500-growth-etf-ivw-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2410702",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:af7bca24e094b:0-should-ishares-s-p-500-growth-etf-ivw-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:d207b9386094b:0",
        "title": "Should Goldman Sachs ActiveBeta U.S. Large Cap Equity ETF (GSLC) Be on Your Investing Radar?",
        "published": 1738840806,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2410705/should-goldman-sachs-activebeta-u-s-large-cap-equity-etf-gslc-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2410705",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:d207b9386094b:0-should-goldman-sachs-activebeta-u-s-large-cap-equity-etf-gslc-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:0eba0c5e0094b:0",
        "title": "Should You Invest in the Invesco Dorsey Wright Technology Momentum ETF (PTF)?",
        "published": 1738754407,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2409778/should-you-invest-in-the-invesco-dorsey-wright-technology-momentum-etf-ptf?cid=CS-TRADINGVIEW-FT-sector_etf-2409778",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:RGTI",
            "logoid": "rigetti-computing-redeemable"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:0eba0c5e0094b:0-should-you-invest-in-the-invesco-dorsey-wright-technology-momentum-etf-ptf/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:236fde077094b:0",
        "title": "Is Franklin U.S. Large Cap Multifactor Index ETF (FLQL) a Strong ETF Right Now?",
        "published": 1738754406,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2409783/is-franklin-u-s-large-cap-multifactor-index-etf-flql-a-strong-etf-right-now?cid=CS-TRADINGVIEW-FT-smart_beta_etf-2409783",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "AMEX:SPY",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "AMEX:VOO",
            "logoid": "vanguard"
          }
        ],
        "storyPath": "/news/zacks:236fde077094b:0-is-franklin-u-s-large-cap-multifactor-index-etf-flql-a-strong-etf-right-now/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:81ef9befa094b:0",
        "title": "Should You Invest in the iShares U.S. Technology ETF (IYW)?",
        "published": 1738754406,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2409782/should-you-invest-in-the-ishares-u-s-technology-etf-iyw?cid=CS-TRADINGVIEW-FT-sector_etf-2409782",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:81ef9befa094b:0-should-you-invest-in-the-ishares-u-s-technology-etf-iyw/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:9ae0d4bad094b:0",
        "title": "How Will Big Tech ETFs Be Impacted by Trump Tariffs?",
        "published": 1738674000,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2408946/how-will-big-tech-etfs-be-impacted-by-trump-tariffs?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2408946",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMD",
            "logoid": "advanced-micro-devices"
          },
          {
            "symbol": "NASDAQ:INTC",
            "logoid": "intel"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          }
        ],
        "storyPath": "/news/zacks:9ae0d4bad094b:0-how-will-big-tech-etfs-be-impacted-by-trump-tariffs/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "leverage_shares:b8b667315094b:0",
        "title": "Apple Reports Record Revenue in Q1 2025",
        "published": 1738604452,
        "urgency": 2,
        "link": "https://leverageshares.com/en-eu/insights/apple-reports-record-revenue-in-q1-2025/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/leverage_shares:b8b667315094b:0-apple-reports-record-revenue-in-q1-2025/",
        "provider": {
          "id": "leverage_shares",
          "name": "Leverage Shares",
          "logo_id": "leverage-shares",
          "url": "https://leverageshares.com/en/"
        }
      },
      {
        "id": "zacks:cce89aa78094b:0",
        "title": "Should Motley Fool 100 Index ETF (TMFC) Be on Your Investing Radar?",
        "published": 1738581623,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2408000/should-motley-fool-100-index-etf-tmfc-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2408000",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:cce89aa78094b:0-should-motley-fool-100-index-etf-tmfc-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:d5e5c1b6a094b:0",
        "title": "Is Schwab Fundamental U.S. Broad Market ETF (FNDB) a Strong ETF Right Now?",
        "published": 1738581621,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2408014/is-schwab-fundamental-u-s-broad-market-etf-fndb-a-strong-etf-right-now?cid=CS-TRADINGVIEW-FT-smart_beta_etf-2408014",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:BRK.A",
            "logoid": "berkshire-hathaway"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          }
        ],
        "storyPath": "/news/zacks:d5e5c1b6a094b:0-is-schwab-fundamental-u-s-broad-market-etf-fndb-a-strong-etf-right-now/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:b169c036c094b:0",
        "title": "ETFs to Ride on Apple's Best-Ever Revenues",
        "published": 1738336260,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2407640/etfs-to-ride-on-apple-s-best-ever-revenues?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2407640",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/zacks:b169c036c094b:0-etfs-to-ride-on-apple-s-best-ever-revenues/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:c6769ac79094b:0",
        "title": "Should Vanguard Russell 1000 ETF (VONE) Be on Your Investing Radar?",
        "published": 1738322408,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2407238/should-vanguard-russell-1000-etf-vone-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2407238",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "BCBA:SPY",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:c6769ac79094b:0-should-vanguard-russell-1000-etf-vone-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:2e7932d3e094b:0",
        "title": "Should ALPS (OUSA) Be on Your Investing Radar?",
        "published": 1738322407,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2407239/should-alps-ousa-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2407239",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:V",
            "logoid": "visa"
          },
          {
            "symbol": "NYSE:HD",
            "logoid": "home-depot"
          }
        ],
        "storyPath": "/news/zacks:2e7932d3e094b:0-should-alps-ousa-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:61e4fb471094b:0",
        "title": "Is ALPS (OUSA) a Strong ETF Right Now?",
        "published": 1738236007,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2406323/is-alps-ousa-a-strong-etf-right-now?cid=CS-TRADINGVIEW-FT-smart_beta_etf-2406323",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:V",
            "logoid": "visa"
          },
          {
            "symbol": "NYSE:HD",
            "logoid": "home-depot"
          }
        ],
        "storyPath": "/news/zacks:61e4fb471094b:0-is-alps-ousa-a-strong-etf-right-now/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:0e777c8fe094b:0",
        "title": "Is iShares U.S. Equity Factor ETF (LRGF) a Strong ETF Right Now?",
        "published": 1738236006,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2406328/is-ishares-u-s-equity-factor-etf-lrgf-a-strong-etf-right-now?cid=CS-TRADINGVIEW-FT-smart_beta_etf-2406328",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:0e777c8fe094b:0-is-ishares-u-s-equity-factor-etf-lrgf-a-strong-etf-right-now/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:8e77127cd094b:0",
        "title": "Should Schwab U.S. Large-Cap ETF (SCHX) Be on Your Investing Radar?",
        "published": 1738149608,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2405177/should-schwab-u-s-large-cap-etf-schx-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2405177",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:8e77127cd094b:0-should-schwab-u-s-large-cap-etf-schx-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:db4ce0b39094b:0",
        "title": "Is Fidelity High Dividend ETF (FDVV) a Strong ETF Right Now?",
        "published": 1738149607,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2405187/is-fidelity-high-dividend-etf-fdvv-a-strong-etf-right-now?cid=CS-TRADINGVIEW-FT-smart_beta_etf-2405187",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:db4ce0b39094b:0-is-fidelity-high-dividend-etf-fdvv-a-strong-etf-right-now/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:85668bae3094b:0",
        "title": "Should You Invest in the Technology Select Sector SPDR ETF (XLK)?",
        "published": 1738149607,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2405185/should-you-invest-in-the-technology-select-sector-spdr-etf-xlk?cid=CS-TRADINGVIEW-FT-sector_etf-2405185",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:85668bae3094b:0-should-you-invest-in-the-technology-select-sector-spdr-etf-xlk/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:cce0d6ade094b:0",
        "title": "Is Invesco Russell 1000 Dynamic Multifactor ETF (OMFL) a Strong ETF Right Now?",
        "published": 1738063208,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2404313/is-invesco-russell-1000-dynamic-multifactor-etf-omfl-a-strong-etf-right-now?cid=CS-TRADINGVIEW-FT-smart_beta_etf-2404313",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          }
        ],
        "storyPath": "/news/zacks:cce0d6ade094b:0-is-invesco-russell-1000-dynamic-multifactor-etf-omfl-a-strong-etf-right-now/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:a0e1b9158094b:0",
        "title": "Is iShares MSCI ACWI Low Carbon Target ETF (CRBN) a Strong ETF Right Now?",
        "published": 1738063206,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2404321/is-ishares-msci-acwi-low-carbon-target-etf-crbn-a-strong-etf-right-now?cid=CS-TRADINGVIEW-FT-smart_beta_etf-2404321",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:BLK",
            "logoid": "blackrock"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:a0e1b9158094b:0-is-ishares-msci-acwi-low-carbon-target-etf-crbn-a-strong-etf-right-now/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:6e77afb3d094b:0",
        "title": "Should SPDR MSCI USA StrategicFactors ETF (QUS) Be on Your Investing Radar?",
        "published": 1738063206,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2404319/should-spdr-msci-usa-strategicfactors-etf-qus-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2404319",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "BCBA:SPY",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          }
        ],
        "storyPath": "/news/zacks:6e77afb3d094b:0-should-spdr-msci-usa-strategicfactors-etf-qus-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:3e207dc80094b:0",
        "title": "Mag 7 ETFs to Watch This Earnings Season",
        "published": 1737990000,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2403891/mag-7-etfs-to-watch-this-earnings-season?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2403891",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          }
        ],
        "storyPath": "/news/zacks:3e207dc80094b:0-mag-7-etfs-to-watch-this-earnings-season/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:dd7483544094b:0",
        "title": "Should BNY Mellon US Large Cap Core Equity ETF (BKLC) Be on Your Investing Radar?",
        "published": 1737976807,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2403538/should-bny-mellon-us-large-cap-core-equity-etf-bklc-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2403538",
        "relatedSymbols": [
          {
            "symbol": "AMEX:BKLC",
            "logoid": "bny-mellon-core-bond-etf"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "AMEX:SPY",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "AMEX:IVV",
            "logoid": "ishares"
          }
        ],
        "storyPath": "/news/zacks:dd7483544094b:0-should-bny-mellon-us-large-cap-core-equity-etf-bklc-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:592ad951c094b:0",
        "title": "Should Goldman Sachs MarketBeta U.S. 1000 Equity ETF (GUSA) Be on Your Investing Radar?",
        "published": 1737717607,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2402674/should-goldman-sachs-marketbeta-u-s-1000-equity-etf-gusa-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2402674",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:592ad951c094b:0-should-goldman-sachs-marketbeta-u-s-1000-equity-etf-gusa-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:f1e229eb8094b:0",
        "title": "Is WisdomTree U.S. LargeCap ETF (EPS) a Strong ETF Right Now?",
        "published": 1737717605,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2402678/is-wisdomtree-u-s-largecap-etf-eps-a-strong-etf-right-now?cid=CS-TRADINGVIEW-FT-smart_beta_etf-2402678",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          }
        ],
        "storyPath": "/news/zacks:f1e229eb8094b:0-is-wisdomtree-u-s-largecap-etf-eps-a-strong-etf-right-now/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:63f34454e094b:0",
        "title": "Should Strive 500 ETF (STRV) Be on Your Investing Radar?",
        "published": 1737631207,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2401832/should-strive-500-etf-strv-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2401832",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:63f34454e094b:0-should-strive-500-etf-strv-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:db65c299e094b:0",
        "title": "Should Invesco Dividend Achievers ETF (PFM) Be on Your Investing Radar?",
        "published": 1737544806,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2400976/should-invesco-dividend-achievers-etf-pfm-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2400976",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AVGO",
            "logoid": "broadcom"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/zacks:db65c299e094b:0-should-invesco-dividend-achievers-etf-pfm-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:52c06fcd7094b:0",
        "title": "Best Investment Strategies for 2025",
        "published": 1737490560,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2400779/best-investment-strategies-for-2025?cid=CS-TRADINGVIEW-FT-etf_spotlight-2400779",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:52c06fcd7094b:0-best-investment-strategies-for-2025/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:ad6eafd07094b:0",
        "title": "Is Fidelity Quality Factor ETF (FQAL) a Strong ETF Right Now?",
        "published": 1737458406,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2400254/is-fidelity-quality-factor-etf-fqal-a-strong-etf-right-now?cid=CS-TRADINGVIEW-FT-smart_beta_etf-2400254",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:ad6eafd07094b:0-is-fidelity-quality-factor-etf-fqal-a-strong-etf-right-now/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:f4b6a2119094b:0",
        "title": "Should First Trust Dow 30 Equal Weight ETF (EDOW) Be on Your Investing Radar?",
        "published": 1737458406,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2400251/should-first-trust-dow-30-equal-weight-etf-edow-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2400251",
        "relatedSymbols": [
          {
            "symbol": "NYSE:BA",
            "logoid": "boeing"
          },
          {
            "symbol": "AMEX:EDOW",
            "logoid": "first-trust"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:CSCO",
            "logoid": "cisco"
          },
          {
            "symbol": "AMEX:SPY",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "AMEX:IVV",
            "logoid": "ishares"
          }
        ],
        "storyPath": "/news/zacks:f4b6a2119094b:0-should-first-trust-dow-30-equal-weight-etf-edow-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:90c82661b094b:0",
        "title": "Should SPDR Portfolio S&P 500 Value ETF (SPYV) Be on Your Investing Radar?",
        "published": 1737372008,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2399548/should-spdr-portfolio-s-p-500-value-etf-spyv-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2399548",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          }
        ],
        "storyPath": "/news/zacks:90c82661b094b:0-should-spdr-portfolio-s-p-500-value-etf-spyv-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:cf025746e094b:0",
        "title": "Should iShares Russell Top 200 ETF (IWL) Be on Your Investing Radar?",
        "published": 1737372006,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2399557/should-ishares-russell-top-200-etf-iwl-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2399557",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:cf025746e094b:0-should-ishares-russell-top-200-etf-iwl-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:fcc38259a094b:0",
        "title": "Should Schwab 1000 Index ETF (SCHK) Be on Your Investing Radar?",
        "published": 1737112808,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2398704/should-schwab-1000-index-etf-schk-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2398704",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:fcc38259a094b:0-should-schwab-1000-index-etf-schk-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:546360c00094b:0",
        "title": "Should iShares Russell 1000 Growth ETF (IWF) Be on Your Investing Radar?",
        "published": 1737026406,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2397918/should-ishares-russell-1000-growth-etf-iwf-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2397918",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:546360c00094b:0-should-ishares-russell-1000-growth-etf-iwf-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:620e79e75094b:0",
        "title": "Should TCW Transform 500 ETF (VOTE) Be on Your Investing Radar?",
        "published": 1736940009,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2397009/should-tcw-transform-500-etf-vote-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2397009",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:620e79e75094b:0-should-tcw-transform-500-etf-vote-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:151ef8dcb094b:0",
        "title": "Is iShares Paris-Aligned Climate MSCI USA ETF (PABU) a Strong ETF Right Now?",
        "published": 1736853608,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2396299/is-ishares-paris-aligned-climate-msci-usa-etf-pabu-a-strong-etf-right-now?cid=CS-TRADINGVIEW-FT-smart_beta_etf-2396299",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:BLK",
            "logoid": "blackrock"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:151ef8dcb094b:0-is-ishares-paris-aligned-climate-msci-usa-etf-pabu-a-strong-etf-right-now/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:831be348c094b:0",
        "title": "Should Vanguard Growth ETF (VUG) Be on Your Investing Radar?",
        "published": 1736853608,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2396296/should-vanguard-growth-etf-vug-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2396296",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:831be348c094b:0-should-vanguard-growth-etf-vug-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:d891c6208094b:0",
        "title": "Should SPDR Portfolio S&P 500 Growth ETF (SPYG) Be on Your Investing Radar?",
        "published": 1736853607,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2396300/should-spdr-portfolio-s-p-500-growth-etf-spyg-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2396300",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:d891c6208094b:0-should-spdr-portfolio-s-p-500-growth-etf-spyg-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:4393a2749094b:0",
        "title": "Should iShares Russell 1000 ETF (IWB) Be on Your Investing Radar?",
        "published": 1736853606,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2396306/should-ishares-russell-1000-etf-iwb-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2396306",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:4393a2749094b:0-should-ishares-russell-1000-etf-iwb-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:d59396868094b:0",
        "title": "Is FlexShares Morningstar U.S. Market Factor Tilt ETF (TILT) a Strong ETF Right Now?",
        "published": 1736767209,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2395501/is-flexshares-morningstar-u-s-market-factor-tilt-etf-tilt-a-strong-etf-right-now?cid=CS-TRADINGVIEW-FT-smart_beta_etf-2395501",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "AMEX:VTI",
            "logoid": "vanguard"
          },
          {
            "symbol": "AMEX:ITOT",
            "logoid": "ishares"
          }
        ],
        "storyPath": "/news/zacks:d59396868094b:0-is-flexshares-morningstar-u-s-market-factor-tilt-etf-tilt-a-strong-etf-right-now/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:8c7b7146a094b:0",
        "title": "Is Schwab Fundamental U.S. Large Company ETF (FNDX) a Strong ETF Right Now?",
        "published": 1736767206,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2395511/is-schwab-fundamental-u-s-large-company-etf-fndx-a-strong-etf-right-now?cid=CS-TRADINGVIEW-FT-smart_beta_etf-2395511",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:BRK.A",
            "logoid": "berkshire-hathaway"
          }
        ],
        "storyPath": "/news/zacks:8c7b7146a094b:0-is-schwab-fundamental-u-s-large-company-etf-fndx-a-strong-etf-right-now/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:ff074333c094b:0",
        "title": "ETF Wisdom From Warren Buffett on Berkshire's 9th Straight Yearly Win",
        "published": 1736445600,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2394648/etf-wisdom-from-warren-buffett-on-berkshire-s-9th-straight-yearly-win?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2394648",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:BRK.A",
            "logoid": "berkshire-hathaway"
          },
          {
            "symbol": "NYSE:BAC",
            "logoid": "bank-of-america"
          }
        ],
        "storyPath": "/news/zacks:ff074333c094b:0-etf-wisdom-from-warren-buffett-on-berkshire-s-9th-straight-yearly-win/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:3081d7026094b:0",
        "title": "Should Vanguard Large-Cap ETF (VV) Be on Your Investing Radar?",
        "published": 1736421609,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2394144/should-vanguard-large-cap-etf-vv-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2394144",
        "relatedSymbols": [
          {
            "symbol": "AMEX:VV",
            "logoid": "vanguard"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "AMEX:SPY",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "AMEX:IVV",
            "logoid": "ishares"
          }
        ],
        "storyPath": "/news/zacks:3081d7026094b:0-should-vanguard-large-cap-etf-vv-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:bd91dee63094b:0",
        "title": "Is WisdomTree U.S. Quality Dividend Growth ETF (DGRW) a Strong ETF Right Now?",
        "published": 1736421607,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2394150/is-wisdomtree-u-s-quality-dividend-growth-etf-dgrw-a-strong-etf-right-now?cid=CS-TRADINGVIEW-FT-smart_beta_etf-2394150",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:DGRW",
            "logoid": "wisdomtree"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AVGO",
            "logoid": "broadcom"
          },
          {
            "symbol": "AMEX:VIG",
            "logoid": "vanguard"
          },
          {
            "symbol": "AMEX:DGRO",
            "logoid": "ishares"
          }
        ],
        "storyPath": "/news/zacks:bd91dee63094b:0-is-wisdomtree-u-s-quality-dividend-growth-etf-dgrw-a-strong-etf-right-now/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:105f684ab094b:0",
        "title": "Is SPDR MSCI USA StrategicFactors ETF (QUS) a Strong ETF Right Now?",
        "published": 1736335208,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2393415/is-spdr-msci-usa-strategicfactors-etf-qus-a-strong-etf-right-now?cid=CS-TRADINGVIEW-FT-smart_beta_etf-2393415",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "BCBA:SPY",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          }
        ],
        "storyPath": "/news/zacks:105f684ab094b:0-is-spdr-msci-usa-strategicfactors-etf-qus-a-strong-etf-right-now/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:3da463251094b:0",
        "title": "Is iShares ESG Aware MSCI USA ETF (ESGU) a Strong ETF Right Now?",
        "published": 1736335206,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2393423/is-ishares-esg-aware-msci-usa-etf-esgu-a-strong-etf-right-now?cid=CS-TRADINGVIEW-FT-smart_beta_etf-2393423",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:3da463251094b:0-is-ishares-esg-aware-msci-usa-etf-esgu-a-strong-etf-right-now/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:07ffc1062094b:0",
        "title": "Is FlexShares Quality Dividend Defensive ETF (QDEF) a Strong ETF Right Now?",
        "published": 1736248808,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2392632/is-flexshares-quality-dividend-defensive-etf-qdef-a-strong-etf-right-now?cid=CS-TRADINGVIEW-FT-smart_beta_etf-2392632",
        "relatedSymbols": [
          {
            "symbol": "AMEX:QDEF",
            "logoid": "flexshares-core-select-bond-fund"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "AMEX:VTI",
            "logoid": "vanguard"
          },
          {
            "symbol": "AMEX:ITOT",
            "logoid": "ishares"
          }
        ],
        "storyPath": "/news/zacks:07ffc1062094b:0-is-flexshares-quality-dividend-defensive-etf-qdef-a-strong-etf-right-now/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:5c9a93e81094b:0",
        "title": "Should Invesco S&P 500 Top 50 ETF (XLG) Be on Your Investing Radar?",
        "published": 1736248808,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2392630/should-invesco-s-p-500-top-50-etf-xlg-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2392630",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "BCBA:SPY",
            "logoid": "spdr-sandp500-etf-tr"
          }
        ],
        "storyPath": "/news/zacks:5c9a93e81094b:0-should-invesco-s-p-500-top-50-etf-xlg-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:eae2649c8094b:0",
        "title": "Should Invesco QQQ (QQQ) Be on Your Investing Radar?",
        "published": 1736248807,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2392633/should-invesco-qqq-qqq-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2392633",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:eae2649c8094b:0-should-invesco-qqq-qqq-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:08bb658a6094b:0",
        "title": "Is Fidelity Value Factor ETF (FVAL) a Strong ETF Right Now?",
        "published": 1736248806,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2392637/is-fidelity-value-factor-etf-fval-a-strong-etf-right-now?cid=CS-TRADINGVIEW-FT-smart_beta_etf-2392637",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:08bb658a6094b:0-is-fidelity-value-factor-etf-fval-a-strong-etf-right-now/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:04a0e10f7094b:0",
        "title": "Should Invesco FTSE RAFI US 1000 ETF (PRF) Be on Your Investing Radar?",
        "published": 1736248806,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2392636/should-invesco-ftse-rafi-us-1000-etf-prf-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2392636",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:BRK.A",
            "logoid": "berkshire-hathaway"
          }
        ],
        "storyPath": "/news/zacks:04a0e10f7094b:0-should-invesco-ftse-rafi-us-1000-etf-prf-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:21ab70876094b:0",
        "title": "Can \"Magnificent Seven\" ETFs Retain Their Glory in 2025?",
        "published": 1736168400,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2392104/can-magnificent-seven-etfs-retain-their-glory-in-2025?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2392104",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          }
        ],
        "storyPath": "/news/zacks:21ab70876094b:0-can-magnificent-seven-etfs-retain-their-glory-in-2025/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:72b0dbdc1094b:0",
        "title": "Is Vanguard Dividend Appreciation ETF (VIG) a Strong ETF Right Now?",
        "published": 1736162408,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2392025/is-vanguard-dividend-appreciation-etf-vig-a-strong-etf-right-now?cid=CS-TRADINGVIEW-FT-smart_beta_etf-2392025",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AVGO",
            "logoid": "broadcom"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          }
        ],
        "storyPath": "/news/zacks:72b0dbdc1094b:0-is-vanguard-dividend-appreciation-etf-vig-a-strong-etf-right-now/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:bd705f841094b:0",
        "title": "Is Invesco S&P 500 Quality ETF (SPHQ) a Strong ETF Right Now?",
        "published": 1736162407,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2392029/is-invesco-s-p-500-quality-etf-sphq-a-strong-etf-right-now?cid=CS-TRADINGVIEW-FT-smart_beta_etf-2392029",
        "relatedSymbols": [
          {
            "symbol": "NYSE:MA",
            "logoid": "mastercard"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:V",
            "logoid": "visa"
          }
        ],
        "storyPath": "/news/zacks:bd705f841094b:0-is-invesco-s-p-500-quality-etf-sphq-a-strong-etf-right-now/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:2f7e7b799094b:0",
        "title": "Should Fidelity Value Factor ETF (FVAL) Be on Your Investing Radar?",
        "published": 1736162406,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2392030/should-fidelity-value-factor-etf-fval-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2392030",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:2f7e7b799094b:0-should-fidelity-value-factor-etf-fval-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:3350d0097094b:0",
        "title": "Should WisdomTree U.S. LargeCap ETF (EPS) Be on Your Investing Radar?",
        "published": 1736162405,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2392034/should-wisdomtree-u-s-largecap-etf-eps-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2392034",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "AMEX:VTV",
            "logoid": "vanguard"
          },
          {
            "symbol": "AMEX:SCHD",
            "logoid": "schwab"
          },
          {
            "symbol": "AMEX:EPS",
            "logoid": "wisdomtree"
          }
        ],
        "storyPath": "/news/zacks:3350d0097094b:0-should-wisdomtree-u-s-largecap-etf-eps-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:eff519513094b:0",
        "title": "What Lies Ahead for Apple Stock & ETFs in 2025?",
        "published": 1735927200,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2391829/what-lies-ahead-for-apple-stock-etfs-in-2025?cid=CS-TRADINGVIEW-FT-etf_news_and_commentary-2391829",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/zacks:eff519513094b:0-what-lies-ahead-for-apple-stock-etfs-in-2025/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:ac99fb059094b:0",
        "title": "Should Fidelity Quality Factor ETF (FQAL) Be on Your Investing Radar?",
        "published": 1735903207,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2391399/should-fidelity-quality-factor-etf-fqal-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2391399",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "BCBA:SPY",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:ac99fb059094b:0-should-fidelity-quality-factor-etf-fqal-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:53aab2a7f094b:0",
        "title": "Should WisdomTree U.S. Total Dividend ETF (DTD) Be on Your Investing Radar?",
        "published": 1735903206,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2391401/should-wisdomtree-u-s-total-dividend-etf-dtd-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2391401",
        "relatedSymbols": [
          {
            "symbol": "NYSE:JPM",
            "logoid": "jpmorgan-chase"
          },
          {
            "symbol": "AMEX:DTD",
            "logoid": "wisdomtree"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "AMEX:VTV",
            "logoid": "vanguard"
          },
          {
            "symbol": "AMEX:SCHD",
            "logoid": "schwab"
          }
        ],
        "storyPath": "/news/zacks:53aab2a7f094b:0-should-wisdomtree-u-s-total-dividend-etf-dtd-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:b72d21504094b:0",
        "title": "Should iShares Core S&P 500 ETF (IVV) Be on Your Investing Radar?",
        "published": 1735816807,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2390545/should-ishares-core-s-p-500-etf-ivv-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2390545",
        "relatedSymbols": [
          {
            "symbol": "AMEX:IVV",
            "logoid": "ishares"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "AMEX:SPY",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "AMEX:VOO",
            "logoid": "vanguard"
          }
        ],
        "storyPath": "/news/zacks:b72d21504094b:0-should-ishares-core-s-p-500-etf-ivv-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:34d23a55c094b:0",
        "title": "Should Vanguard S&P 500 ETF (VOO) Be on Your Investing Radar?",
        "published": 1735730408,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2390295/should-vanguard-s-p-500-etf-voo-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2390295",
        "relatedSymbols": [
          {
            "symbol": "AMEX:VOO",
            "logoid": "vanguard"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "AMEX:SPY",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "AMEX:IVV",
            "logoid": "ishares"
          }
        ],
        "storyPath": "/news/zacks:34d23a55c094b:0-should-vanguard-s-p-500-etf-voo-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:452f91e0d094b:0",
        "title": "Should Vanguard S&P 500 Growth ETF (VOOG) Be on Your Investing Radar?",
        "published": 1735730408,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2390296/should-vanguard-s-p-500-growth-etf-voog-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2390296",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:452f91e0d094b:0-should-vanguard-s-p-500-growth-etf-voog-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:3dd7ffb8d094b:0",
        "title": "Is iShares MSCI USA Quality Factor ETF (QUAL) a Strong ETF Right Now?",
        "published": 1735644008,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2389814/is-ishares-msci-usa-quality-factor-etf-qual-a-strong-etf-right-now?cid=CS-TRADINGVIEW-FT-smart_beta_etf-2389814",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:3dd7ffb8d094b:0-is-ishares-msci-usa-quality-factor-etf-qual-a-strong-etf-right-now/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:6720a86ac094b:0",
        "title": "Should Fidelity Nasdaq Composite Index ETF (ONEQ) Be on Your Investing Radar?",
        "published": 1735644008,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2389812/should-fidelity-nasdaq-composite-index-etf-oneq-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2389812",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:6720a86ac094b:0-should-fidelity-nasdaq-composite-index-etf-oneq-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:fba111a5f094b:0",
        "title": "Should Vanguard Mega Cap ETF (MGC) Be on Your Investing Radar?",
        "published": 1735644007,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2389815/should-vanguard-mega-cap-etf-mgc-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2389815",
        "relatedSymbols": [
          {
            "symbol": "AMEX:MGC",
            "logoid": "vanguard"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "AMEX:SPY",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "AMEX:IVV",
            "logoid": "ishares"
          }
        ],
        "storyPath": "/news/zacks:fba111a5f094b:0-should-vanguard-mega-cap-etf-mgc-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:4c4e152b0094b:0",
        "title": "Should SPDR S&P 500 ETF (SPY) Be on Your Investing Radar?",
        "published": 1735557609,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2389221/should-spdr-s-p-500-etf-spy-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2389221",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "BCBA:SPY",
            "logoid": "spdr-sandp500-etf-tr"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:4c4e152b0094b:0-should-spdr-s-p-500-etf-spy-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:dcaa02ac7094b:0",
        "title": "Is Franklin U.S. Equity Index ETF (USPX) a Strong ETF Right Now?",
        "published": 1735557608,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2389226/is-franklin-u-s-equity-index-etf-uspx-a-strong-etf-right-now?cid=CS-TRADINGVIEW-FT-smart_beta_etf-2389226",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:dcaa02ac7094b:0-is-franklin-u-s-equity-index-etf-uspx-a-strong-etf-right-now/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:0fa4d4d8a094b:0",
        "title": "Should iShares Russell Top 200 Growth ETF (IWY) Be on Your Investing Radar?",
        "published": 1735557607,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2389228/should-ishares-russell-top-200-growth-etf-iwy-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2389228",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/zacks:0fa4d4d8a094b:0-should-ishares-russell-top-200-growth-etf-iwy-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:9aa4af605094b:0",
        "title": "Is FlexShares Quality Dividend ETF (QDF) a Strong ETF Right Now?",
        "published": 1735557606,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2389234/is-flexshares-quality-dividend-etf-qdf-a-strong-etf-right-now?cid=CS-TRADINGVIEW-FT-smart_beta_etf-2389234",
        "relatedSymbols": [
          {
            "symbol": "AMEX:QDF",
            "logoid": "flexshares-core-select-bond-fund"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "AMEX:VTI",
            "logoid": "vanguard"
          },
          {
            "symbol": "AMEX:ITOT",
            "logoid": "ishares"
          }
        ],
        "storyPath": "/news/zacks:9aa4af605094b:0-is-flexshares-quality-dividend-etf-qdf-a-strong-etf-right-now/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:4ad42f709094b:0",
        "title": "Should iShares S&P 100 ETF (OEF) Be on Your Investing Radar?",
        "published": 1735039208,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2387256/should-ishares-s-p-100-etf-oef-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2387256",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "BCBA:SPY",
            "logoid": "spdr-sandp500-etf-tr"
          }
        ],
        "storyPath": "/news/zacks:4ad42f709094b:0-should-ishares-s-p-100-etf-oef-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      },
      {
        "id": "zacks:77a713f17094b:0",
        "title": "Should Vanguard Mega Cap Growth ETF (MGK) Be on Your Investing Radar?",
        "published": 1735039207,
        "urgency": 2,
        "link": "https://www.zacks.com/stock/news/2387263/should-vanguard-mega-cap-growth-etf-mgk-be-on-your-investing-radar?cid=CS-TRADINGVIEW-FT-style_box_etf-2387263",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:QQQ",
            "logoid": "invesco"
          },
          {
            "symbol": "AMEX:MGK",
            "logoid": "vanguard"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "AMEX:VUG",
            "logoid": "vanguard"
          }
        ],
        "storyPath": "/news/zacks:77a713f17094b:0-should-vanguard-mega-cap-growth-etf-mgk-be-on-your-investing-radar/",
        "provider": {
          "id": "zacks",
          "name": "Zacks",
          "logo_id": "zacks",
          "url": "http://www.zacks.com/"
        }
      }
    ],
    "streaming": {
      "channel": "2cc85ad3d7cfbe99f680dc8a9b32"
    },
    "pagination": {
      "cursor": "eyJfaWQiOiJ6YWNrczpjN2U1NDZjMmUwOTRiIiwicHViZGF0ZSI6MTczMzQ4NDAwNzAwMH0="
    }
  },
  "msg": "Success"
}
```

## Get Forex News

`GET /api/news/forex`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/api/news/forex?symbol=NASDAQ%3AAAPL&lang=en' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "invezz:5bb71649d094b:0",
        "title": "European stocks fall as Trump proposes 50% tariff on EU imports; says talks with them ‘going nowhere’",
        "published": 1748007559,
        "urgency": 2,
        "link": "https://invezz.com/news/2025/05/23/european-stocks-fall-as-trump-proposes-50-tariff-on-eu-imports-says-talks-with-them-going-nowhere/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/invezz:5bb71649d094b:0-european-stocks-fall-as-trump-proposes-50-tariff-on-eu-imports-says-talks-with-them-going-nowhere/",
        "provider": {
          "id": "invezz",
          "name": "Invezz",
          "logo_id": "invezz",
          "url": "https://invezz.com/"
        }
      },
      {
        "id": "invezz:4deb6e0a7094b:0",
        "title": "Apple and Meta face €1.8B enforcement action for EU DMA breaches",
        "published": 1745408010,
        "urgency": 2,
        "link": "https://invezz.com/news/2025/04/23/apple-and-meta-face-e1-8b-enforcement-action-for-eu-dma-breaches/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "FX:EURUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "country/EU"
          }
        ],
        "storyPath": "/news/invezz:4deb6e0a7094b:0-apple-and-meta-face-1-8b-enforcement-action-for-eu-dma-breaches/",
        "provider": {
          "id": "invezz",
          "name": "Invezz",
          "logo_id": "invezz",
          "url": "https://invezz.com/"
        }
      }
    ],
    "streaming": {
      "channel": "b69b9baeb07bb717724e553c947c"
    }
  },
  "msg": "Success"
}
```

## Get Futures News

`GET /api/news/futures`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/api/news/futures?symbol=NASDAQ%3AAAPL&lang=en' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "DJN_DN20260227008205:0",
        "title": "How to Fight AI? The 'Rolex Effect' Could Lift Apple and Other Consumer Brands — Barrons.com",
        "published": 1772213100,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:MCD",
            "logoid": "mcdonalds"
          },
          {
            "symbol": "NASDAQ:WMT",
            "logoid": "walmart"
          }
        ],
        "storyPath": "/news/DJN_DN20260227008205:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260217003591:0",
        "title": "Gold Buying Is Most Crowded Trade, BofA Survey Says — Market Talk",
        "published": 1771331160,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          }
        ],
        "storyPath": "/news/DJN_DN20260217003591:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L1N3X20U6:0",
        "title": "US group sues Apple over Congo conflict minerals",
        "published": 1764193852,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L1N3X20U6:0-us-group-sues-apple-over-congo-conflict-minerals/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L8N3WT0FU:0",
        "title": "Congo extends ban on trade in minerals from sites in war-hit east",
        "published": 1763384901,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NYSE:DELL",
            "logoid": "dell"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L8N3WT0FU:0-congo-extends-ban-on-trade-in-minerals-from-sites-in-war-hit-east/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2025:newsml_L6N3QI0JZ:0",
        "title": "Big Tech, US card firms, copper miners",
        "published": 1743781786,
        "urgency": 2,
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "DJ:DJI",
            "logoid": "indices/dow-30"
          },
          {
            "symbol": "SP:SPX",
            "logoid": "indices/s-and-p-500"
          },
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "NYSE:NVR",
            "logoid": "nvr"
          },
          {
            "symbol": "NYSE:DECK",
            "logoid": "deckers-outdoor"
          },
          {
            "symbol": "NYSE:DHI",
            "logoid": "dr-horton"
          },
          {
            "symbol": "NASDAQ:APA",
            "logoid": "apa-corporation"
          },
          {
            "symbol": "NASDAQ:GEHC",
            "logoid": "ge-healthcare-technologies"
          },
          {
            "symbol": "NYSE:DD",
            "logoid": "dupont-de-nemours"
          },
          {
            "symbol": "NYSE:LOCL",
            "logoid": "local-bounti"
          },
          {
            "symbol": "NYSE:GES"
          },
          {
            "symbol": "NYSE:IBP",
            "logoid": "installed-building-products"
          },
          {
            "symbol": "NYSE:TSE"
          },
          {
            "symbol": "NYSE:NBR",
            "logoid": "nabors-industries"
          },
          {
            "symbol": "NYSE:KOS",
            "logoid": "kosmos-energy"
          },
          {
            "symbol": "NASDAQ:AREB",
            "logoid": "american-rebel"
          },
          {
            "symbol": "NASDAQ:SOBR",
            "logoid": "sobr-safe"
          },
          {
            "symbol": "NASDAQ:RSLS"
          },
          {
            "symbol": "NASDAQ:NMTC",
            "logoid": "neuroone-medical-technologies"
          },
          {
            "symbol": "NASDAQ:APVO",
            "logoid": "aptevo-therapeutics"
          },
          {
            "symbol": "NASDAQ:MRM",
            "logoid": "medirom-healthcare-technologies"
          },
          {
            "symbol": "SP:S5INFT",
            "logoid": "sector/information-technology"
          },
          {
            "symbol": "SP:S5UTIL",
            "logoid": "sector/utilities"
          },
          {
            "symbol": "SP:S5COND",
            "logoid": "sector/consumer-discretionary"
          },
          {
            "symbol": "SP:S5MATR",
            "logoid": "sector/materials"
          },
          {
            "symbol": "SP:S5INDU",
            "logoid": "sector/industrial"
          },
          {
            "symbol": "SP:S5TELS",
            "logoid": "sector/communication-services"
          },
          {
            "symbol": "SP:SPF",
            "logoid": "sector/financial"
          },
          {
            "symbol": "SP:S5REAS",
            "logoid": "sector/real-estate"
          },
          {
            "symbol": "SP:S5HLTH",
            "logoid": "sector/health-care"
          },
          {
            "symbol": "SP:S5CONS",
            "logoid": "sector/consumer-staples"
          },
          {
            "symbol": "SP:SPN",
            "logoid": "sector/energy"
          },
          {
            "symbol": "NYSE:FLG",
            "logoid": "new-york-community"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:FCX",
            "logoid": "freeport-mcmoran"
          },
          {
            "symbol": "NYSE:GS",
            "logoid": "golden-sachs-etf-trust-goldman"
          },
          {
            "symbol": "NYSE:WFC",
            "logoid": "wells-fargo"
          },
          {
            "symbol": "NYSE:SCCO",
            "logoid": "southern-copper"
          },
          {
            "symbol": "NYSE:BABA",
            "logoid": "alibaba"
          },
          {
            "symbol": "NYSE:CVX",
            "logoid": "chevron"
          },
          {
            "symbol": "NASDAQ:PDD",
            "logoid": "pinduoduo"
          },
          {
            "symbol": "NASDAQ:NTES",
            "logoid": "netease"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NYSE:JPM",
            "logoid": "jpmorgan-chase"
          },
          {
            "symbol": "NYSE:XOM",
            "logoid": "exxon"
          },
          {
            "symbol": "LSE:RIO",
            "logoid": "rio-tinto"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "TVC:DJI",
            "logoid": "indices/dow-30"
          },
          {
            "symbol": "ASX:BHP",
            "logoid": "bhp"
          },
          {
            "symbol": "NYSE:BAC",
            "logoid": "bank-of-america"
          },
          {
            "symbol": "NASDAQ:JD",
            "logoid": "jd-com"
          }
        ],
        "storyPath": "/news/reuters.com,2025:newsml_L6N3QI0JZ:0-big-tech-us-card-firms-copper-miners/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      }
    ],
    "streaming": {
      "channel": "769c5fc64e9c84c9374f4c551d2d"
    }
  },
  "msg": "Success"
}
```

## Get Index News

`GET /api/news/index`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/api/news/index?symbol=NASDAQ%3AAAPL&lang=en' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "DJN_DN20260420009019:0",
        "title": "How Apple Stock Has Fared Under Tim Cook — WSJ",
        "published": 1776724080,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260420009019:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260417005980:0",
        "title": "Stocks Hit Records on Iran Truce Hopes. Why the Rally May Have Further to Run. — Barrons.com",
        "published": 1776451200,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          }
        ],
        "storyPath": "/news/DJN_DN20260417005980:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_SN20260417006000:0",
        "title": "These two sectors have been boosted by AI hopes. Why investors should buy one, and trim exposure to the other.",
        "published": 1776432720,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          }
        ],
        "storyPath": "/news/DJN_SN20260417006000:0/",
        "provider": {
          "id": "market-watch",
          "name": "MarketWatch",
          "logo_id": "marketwatch"
        }
      },
      {
        "id": "DJN_DN20260415008356:0",
        "title": "The S&P 500 Just Surged to a Record High Despite a War. Why It May Keep Rising. — Barrons.com",
        "published": 1776286620,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "CBOE:SPX",
            "logoid": "indices/s-and-p-500"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          }
        ],
        "storyPath": "/news/DJN_DN20260415008356:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L1N40T08B:0",
        "title": "Apple leads global smartphone shipments in first quarter, Counterpoint says",
        "published": 1775811689,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L1N40T08B:0-apple-leads-global-smartphone-shipments-in-first-quarter-counterpoint-says/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_SN20260409009895:0",
        "title": "Big Tech stocks look like especially good deals as investors eye what is next for the market",
        "published": 1775748840,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:PLTR",
            "logoid": "palantir"
          }
        ],
        "storyPath": "/news/DJN_SN20260409009895:0/",
        "provider": {
          "id": "market-watch",
          "name": "MarketWatch",
          "logo_id": "marketwatch"
        }
      },
      {
        "id": "DJN_DN20260408006647:0",
        "title": "How Wall Street Went from Iran War Angst to Watching for a New S&P 500 Record — Barrons.com",
        "published": 1775667540,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "CBOE:SPX",
            "logoid": "indices/s-and-p-500"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NYSE:JPM",
            "logoid": "jpmorgan-chase"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          }
        ],
        "storyPath": "/news/DJN_DN20260408006647:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260407004684:0",
        "title": "The Dow Tests a Key Technical Threshold. Watching Apple, Home Depot Stocks. — Barrons.com",
        "published": 1775574120,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:HD",
            "logoid": "home-depot"
          }
        ],
        "storyPath": "/news/DJN_DN20260407004684:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260407004477:0",
        "title": "Apple Stock Drags Down the Dow — WSJ",
        "published": 1775572500,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "TVC:DJI",
            "logoid": "indices/dow-30"
          }
        ],
        "storyPath": "/news/DJN_DN20260407004477:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260407000359:0",
        "title": "Big Tech and Banks Expected to Lead Solid Earnings Season. There Will Be Buying Opportunities. — Barrons.com",
        "published": 1775541600,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AVGO",
            "logoid": "broadcom"
          },
          {
            "symbol": "NYSE:JPM",
            "logoid": "jpmorgan-chase"
          },
          {
            "symbol": "NYSE:MS",
            "logoid": "morgan-stanley"
          }
        ],
        "storyPath": "/news/DJN_DN20260407000359:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN40P0KO:0",
        "title": "Foldable iPhone Hits Engineering Snags, Shipment Delays Possible- Nikkei Asia",
        "published": 1775529722,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN40P0KO:0-foldable-iphone-hits-engineering-snags-shipment-delays-possible-nikkei-asia/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_SN20260403003137:0",
        "title": "Why the stock market has struggled without Big Tech's leadership",
        "published": 1775229480,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_SN20260403003137:0/",
        "provider": {
          "id": "market-watch",
          "name": "MarketWatch",
          "logo_id": "marketwatch"
        }
      },
      {
        "id": "DJN_DN20260319006750:0",
        "title": "These Tech Stocks Are Still a Buy for Many People Even as Iran War Pullback Intensifies — Barrons.com",
        "published": 1773948420,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:XOM",
            "logoid": "exxon"
          },
          {
            "symbol": "NASDAQ:MU",
            "logoid": "micron-technology"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/DJN_DN20260319006750:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_SN20260226013776:0",
        "title": "These S&P 500 alternatives have shined so far this year",
        "published": 1772122560,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "CBOE:SPX",
            "logoid": "indices/s-and-p-500"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "AMEX:RSP",
            "logoid": "invesco"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/DJN_SN20260226013776:0/",
        "provider": {
          "id": "market-watch",
          "name": "MarketWatch",
          "logo_id": "marketwatch"
        }
      },
      {
        "id": "DJN_DN20260202007379:0",
        "title": "Why the S&P 500 at 7000 Is Raising Red Flags — Barrons.com",
        "published": 1770056700,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "CBOE:SPX",
            "logoid": "indices/s-and-p-500"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          }
        ],
        "storyPath": "/news/DJN_DN20260202007379:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L6N3YU0IL:0",
        "title": "Global shares gain on earnings optimism, gold surges ahead ",
        "published": 1769678881,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "TVC:SXXP",
            "logoid": "indices/stoxx-600"
          },
          {
            "symbol": "BME:IBC",
            "logoid": "indices/ibex-35"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "CME_MINI:ES1!",
            "logoid": "indices/s-and-p-500"
          },
          {
            "symbol": "CME_MINI:NQ1!",
            "logoid": "indices/nasdaq-100"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "TVC:GOLD",
            "logoid": "metal/gold"
          },
          {
            "symbol": "ICEEUR:BRN1!",
            "logoid": "crude-oil"
          },
          {
            "symbol": "NYMEX:CL1!",
            "logoid": "crude-oil"
          },
          {
            "symbol": "KRX:KOSPI",
            "logoid": "indices/korea-composite-index"
          },
          {
            "symbol": "IDX:COMPOSITE",
            "logoid": "indices/jakarta-composite-index"
          },
          {
            "symbol": "TVC:DXY",
            "logoid": "indices/u-s-dollar-index"
          },
          {
            "symbol": "FX:EURUSD",
            "currency-logoid": "country/US",
            "base-currency-logoid": "country/EU"
          },
          {
            "symbol": "FX_IDC:USDCHF",
            "currency-logoid": "country/CH",
            "base-currency-logoid": "country/US"
          },
          {
            "symbol": "FX_IDC:USDJPY",
            "currency-logoid": "country/JP",
            "base-currency-logoid": "country/US"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L6N3YU0IL:0-global-shares-gain-on-earnings-optimism-gold-surges-ahead/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "moneycontrol:22760eb43094b:0",
        "title": "Nasdaq suffers sharpest slide in eight months in November as AI stocks retreat",
        "published": 1763457555,
        "urgency": 2,
        "link": "https://www.moneycontrol.com/news/business/earnings/nasdaq-suffers-sharpest-slide-in-eight-months-in-november-as-ai-stocks-retreat-13683110.html",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/moneycontrol:22760eb43094b:0-nasdaq-suffers-sharpest-slide-in-eight-months-in-november-as-ai-stocks-retreat/",
        "provider": {
          "id": "moneycontrol",
          "name": "Moneycontrol",
          "logo_id": "moneycontrol"
        }
      },
      {
        "id": "moneycontrol:7ed33732a094b:0",
        "title": "AI boom fuels 75% of S&P 500 gains since ChatGPT launch in 2022",
        "published": 1759225884,
        "urgency": 2,
        "link": "https://www.moneycontrol.com/news/business/markets/ai-boom-fuels-75-of-s-p-500-gains-since-chatgpt-launch-in-2022-13590200.html",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NYSE:JPM",
            "logoid": "jpmorgan-chase"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          }
        ],
        "storyPath": "/news/moneycontrol:7ed33732a094b:0-ai-boom-fuels-75-of-s-p-500-gains-since-chatgpt-launch-in-2022/",
        "provider": {
          "id": "moneycontrol",
          "name": "Moneycontrol",
          "logo_id": "moneycontrol"
        }
      },
      {
        "id": "moneycontrol:8569a99c3094b:0",
        "title": "Wall Street Futures fall as Trump's new tariffs and Amazon earnings weigh; labor market data awaited",
        "published": 1754051540,
        "urgency": 2,
        "link": "https://www.moneycontrol.com/news/business/markets/wall-street-futures-fall-as-trump-s-new-tariffs-and-amazon-earnings-weigh-labor-market-data-awaited-13370962.html",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          }
        ],
        "storyPath": "/news/moneycontrol:8569a99c3094b:0-wall-street-futures-fall-as-trump-s-new-tariffs-and-amazon-earnings-weigh-labor-market-data-awaited/",
        "provider": {
          "id": "moneycontrol",
          "name": "Moneycontrol",
          "logo_id": "moneycontrol"
        }
      },
      {
        "id": "moneycontrol:4ab15a6f6094b:0",
        "title": "Wall street extends rally as strong jobs data tempers recession worries",
        "published": 1746196136,
        "urgency": 2,
        "link": "https://www.moneycontrol.com/news/business/markets/wall-street-extends-rally-as-strong-jobs-data-tempers-recession-worries-13011783.html",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "DJ:DJI",
            "logoid": "indices/dow-30"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/moneycontrol:4ab15a6f6094b:0-wall-street-extends-rally-as-strong-jobs-data-tempers-recession-worries/",
        "provider": {
          "id": "moneycontrol",
          "name": "Moneycontrol",
          "logo_id": "moneycontrol"
        }
      },
      {
        "id": "moneycontrol:5e52ffacf094b:0",
        "title": "Wall Street edges higher even as trade negotiations and tech earnings keep investors on edge",
        "published": 1745943975,
        "urgency": 2,
        "link": "https://www.moneycontrol.com/news/business/markets/wall-street-edges-higher-even-as-trade-negotiations-and-tech-earnings-keep-investors-on-edge-13008521.html",
        "relatedSymbols": [
          {
            "symbol": "NYSE:GM",
            "logoid": "general-motors"
          },
          {
            "symbol": "NASDAQ:AAL",
            "logoid": "american-airlines-group"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "DJ:DJI",
            "logoid": "indices/dow-30"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:SKX"
          }
        ],
        "storyPath": "/news/moneycontrol:5e52ffacf094b:0-wall-street-edges-higher-even-as-trade-negotiations-and-tech-earnings-keep-investors-on-edge/",
        "provider": {
          "id": "moneycontrol",
          "name": "Moneycontrol",
          "logo_id": "moneycontrol"
        }
      },
      {
        "id": "moneycontrol:78632e842094b:0",
        "title": "Wall Street opens flat as investors await big tech earnings this week",
        "published": 1745936711,
        "urgency": 2,
        "link": "https://www.moneycontrol.com/news/business/markets/wall-street-opens-flat-as-investors-await-big-tech-earnings-this-week-13008481.html",
        "relatedSymbols": [
          {
            "symbol": "NYSE:GM",
            "logoid": "general-motors"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "DJ:DJI",
            "logoid": "indices/dow-30"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/moneycontrol:78632e842094b:0-wall-street-opens-flat-as-investors-await-big-tech-earnings-this-week/",
        "provider": {
          "id": "moneycontrol",
          "name": "Moneycontrol",
          "logo_id": "moneycontrol"
        }
      },
      {
        "id": "moneycontrol:5c930df21094b:0",
        "title": "Wall Street futures mixed as investors await big tech earnings this week",
        "published": 1745929619,
        "urgency": 2,
        "link": "https://www.moneycontrol.com/news/business/markets/wall-street-futures-mixed-as-investors-await-big-tech-earnings-this-week-13008396.html",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "DJ:DJI",
            "logoid": "indices/dow-30"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:NDAQ",
            "logoid": "nasdaq"
          }
        ],
        "storyPath": "/news/moneycontrol:5c930df21094b:0-wall-street-futures-mixed-as-investors-await-big-tech-earnings-this-week/",
        "provider": {
          "id": "moneycontrol",
          "name": "Moneycontrol",
          "logo_id": "moneycontrol"
        }
      },
      {
        "id": "moneycontrol:ceed347a8094b:0",
        "title": "S&P500, Nasdaq Composite slip ahead of tech earnings; Dow Jones adds 150 pts",
        "published": 1745851313,
        "urgency": 2,
        "link": "https://www.moneycontrol.com/news/business/markets/s-p500-nasdaq-composite-slip-ahead-of-tech-earnings-dow-jones-adds-150-pts-13007339.html",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "DJ:DJI",
            "logoid": "indices/dow-30"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/moneycontrol:ceed347a8094b:0-s-p500-nasdaq-composite-slip-ahead-of-tech-earnings-dow-jones-adds-150-pts/",
        "provider": {
          "id": "moneycontrol",
          "name": "Moneycontrol",
          "logo_id": "moneycontrol"
        }
      },
      {
        "id": "moneycontrol:90b1d321a094b:0",
        "title": "Wall Street off to a flying start as Trump signals softer tone on Powell and China tariffs",
        "published": 1745416148,
        "urgency": 2,
        "link": "https://www.moneycontrol.com/news/business/markets/wall-street-off-to-a-flying-start-as-trump-signals-softer-tone-on-powell-and-china-tariffs-13002348.html",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:NDAQ",
            "logoid": "nasdaq"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NYSE:DOW",
            "logoid": "dow"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/moneycontrol:90b1d321a094b:0-wall-street-off-to-a-flying-start-as-trump-signals-softer-tone-on-powell-and-china-tariffs/",
        "provider": {
          "id": "moneycontrol",
          "name": "Moneycontrol",
          "logo_id": "moneycontrol"
        }
      },
      {
        "id": "moneycontrol:dbe6e83b7094b:0",
        "title": "US index futures higher by 1.5 percent on temporary tariff relief on electronics",
        "published": 1744633408,
        "urgency": 2,
        "link": "https://www.moneycontrol.com/news/business/markets/us-index-futures-higher-by-1-5-percent-on-temporary-tariff-relief-on-electronics-12993735.html",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/moneycontrol:dbe6e83b7094b:0-us-index-futures-higher-by-1-5-percent-on-temporary-tariff-relief-on-electronics/",
        "provider": {
          "id": "moneycontrol",
          "name": "Moneycontrol",
          "logo_id": "moneycontrol"
        }
      },
      {
        "id": "moneycontrol:c09ad5547094b:0",
        "title": "S&P 500’s 2024 rally shocked forecasters expecting it to fizzle",
        "published": 1735490446,
        "urgency": 2,
        "link": "https://www.moneycontrol.com/news/business/markets/s-p-500-s-2024-rally-shocked-forecasters-expecting-it-to-fizzle-12899757.html",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          }
        ],
        "storyPath": "/news/moneycontrol:c09ad5547094b:0-s-p-500-s-2024-rally-shocked-forecasters-expecting-it-to-fizzle/",
        "provider": {
          "id": "moneycontrol",
          "name": "Moneycontrol",
          "logo_id": "moneycontrol"
        }
      },
      {
        "id": "leverage_shares:a63c6013c094b:0",
        "title": "Nvidia’s Stock Drops Following Q3 Earnings",
        "published": 1733249272,
        "urgency": 2,
        "link": "https://leverageshares.com/en-eu/insights/nvidias-stock-drops-following-q3-earnings/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NDAQ",
            "logoid": "nasdaq"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NYSE:BLK",
            "logoid": "blackrock"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/leverage_shares:a63c6013c094b:0-nvidia-s-stock-drops-following-q3-earnings/",
        "provider": {
          "id": "leverage_shares",
          "name": "Leverage Shares",
          "logo_id": "leverage-shares",
          "url": "https://leverageshares.com/en/"
        }
      },
      {
        "id": "moneycontrol:e416215d4094b:0",
        "title": "US elections: With 38% returns this year, US-focused Indian mutual funds offer better geographical diversification",
        "published": 1730815471,
        "urgency": 2,
        "link": "https://www.moneycontrol.com/news/business/personal-finance/us-focused-mfs-delivered-better-returns-12858764.html",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          }
        ],
        "storyPath": "/news/moneycontrol:e416215d4094b:0-us-elections-with-38-returns-this-year-us-focused-indian-mutual-funds-offer-better-geographical-diversification/",
        "provider": {
          "id": "moneycontrol",
          "name": "Moneycontrol",
          "logo_id": "moneycontrol"
        }
      },
      {
        "id": "moneycontrol:09f60d2fd094b:0",
        "title": "Nasdaq, S&P 500 fall 3% each amid US recession fears, Apple drop",
        "published": 1722905787,
        "urgency": 2,
        "link": "https://www.moneycontrol.com/news/business/markets/nasdaq-sp-500-fall-3-each-amid-us-recession-fears-apple-drop-12787879.html",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NYSE:BRK.A",
            "logoid": "berkshire-hathaway"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "TVC:DJI",
            "logoid": "indices/dow-30"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NDAQ",
            "logoid": "nasdaq"
          }
        ],
        "storyPath": "/news/moneycontrol:09f60d2fd094b:0-nasdaq-s-p-500-fall-3-each-amid-us-recession-fears-apple-drop/",
        "provider": {
          "id": "moneycontrol",
          "name": "Moneycontrol",
          "logo_id": "moneycontrol"
        }
      },
      {
        "id": "moneycontrol:8ab3011fc094b:0",
        "title": "Nasdaq, S&P 500 ride chip-stock wave before Fed decision; Microsoft falters",
        "published": 1722446691,
        "urgency": 2,
        "link": "https://www.moneycontrol.com/news/business/markets/nasdaq-s-microsoft-falters-12783709.html",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMD",
            "logoid": "advanced-micro-devices"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NYSE:DOW",
            "logoid": "dow"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NDAQ",
            "logoid": "nasdaq"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          }
        ],
        "storyPath": "/news/moneycontrol:8ab3011fc094b:0-nasdaq-s-p-500-ride-chip-stock-wave-before-fed-decision-microsoft-falters/",
        "provider": {
          "id": "moneycontrol",
          "name": "Moneycontrol",
          "logo_id": "moneycontrol"
        }
      },
      {
        "id": "moneycontrol:b0c276e83094b:0",
        "title": "Tech earnings drag S&P and Nasdaq lower as Dow inches up amid market caution",
        "published": 1722390407,
        "urgency": 2,
        "link": "https://www.moneycontrol.com/news/business/markets/tech-earnings-drag-sp-and-nasdaq-lower-as-dow-inches-up-amid-market-caution-12782718.html",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "TVC:DJI",
            "logoid": "indices/dow-30"
          }
        ],
        "storyPath": "/news/moneycontrol:b0c276e83094b:0-tech-earnings-drag-s-p-and-nasdaq-lower-as-dow-inches-up-amid-market-caution/",
        "provider": {
          "id": "moneycontrol",
          "name": "Moneycontrol",
          "logo_id": "moneycontrol"
        }
      },
      {
        "id": "moneycontrol:ec96c6889094b:0",
        "title": "US markets extend gains ahead of tech earnings, Fed rate decision, S&P 500 up 0.25%; GIFT Nifty falls",
        "published": 1722270915,
        "urgency": 2,
        "link": "https://www.moneycontrol.com/news/business/markets/us-markets-extend-gains-ahead-of-tech-earnings-fed-rate-decision-s-gift-nifty-falls-12781627.html",
        "relatedSymbols": [
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "TVC:DJI",
            "logoid": "indices/dow-30"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          }
        ],
        "storyPath": "/news/moneycontrol:ec96c6889094b:0-us-markets-extend-gains-ahead-of-tech-earnings-fed-rate-decision-s-p-500-up-0-25-gift-nifty-falls/",
        "provider": {
          "id": "moneycontrol",
          "name": "Moneycontrol",
          "logo_id": "moneycontrol"
        }
      },
      {
        "id": "moneycontrol:2eff26197094b:0",
        "title": "European and U.S. stocks bounce after heavy sell-off as US inflation cools",
        "published": 1722002899,
        "urgency": 2,
        "link": "https://www.moneycontrol.com/news/world/european-and-u-s-stocks-bounce-after-heavy-sell-off-as-us-inflation-cools-12779728.html",
        "relatedSymbols": [
          {
            "symbol": "TVC:UKX",
            "logoid": "indices/uk-100"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "LSE:HSBA",
            "logoid": "hsbc"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NDAQ",
            "logoid": "nasdaq"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          }
        ],
        "storyPath": "/news/moneycontrol:2eff26197094b:0-european-and-u-s-stocks-bounce-after-heavy-sell-off-as-us-inflation-cools/",
        "provider": {
          "id": "moneycontrol",
          "name": "Moneycontrol",
          "logo_id": "moneycontrol"
        }
      },
      {
        "id": "moneycontrol:36fc890e7094b:0",
        "title": "S&P 500 snaps longest streak without a 2% decline since 2007",
        "published": 1721869747,
        "urgency": 2,
        "link": "https://www.moneycontrol.com/news/business/markets/sp-500-snaps-longest-streak-without-a-2-decline-since-2007-12777615.html",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          }
        ],
        "storyPath": "/news/moneycontrol:36fc890e7094b:0-s-p-500-snaps-longest-streak-without-a-2-decline-since-2007/",
        "provider": {
          "id": "moneycontrol",
          "name": "Moneycontrol",
          "logo_id": "moneycontrol"
        }
      },
      {
        "id": "moneycontrol:fb0a5811e094b:0",
        "title": "Dow reaches fresh high, S&P 500 and Nasdaq recover after higher-than-expected PPI data; GIFT Nifty up",
        "published": 1720802633,
        "urgency": 2,
        "link": "https://www.moneycontrol.com/news/business/markets/dow-reaches-fresh-high-s-gift-nifty-up-12768157.html",
        "relatedSymbols": [
          {
            "symbol": "NSE:TCS",
            "logoid": "tata"
          },
          {
            "symbol": "NSE:WIPRO",
            "logoid": "wipro"
          },
          {
            "symbol": "NSE:INFY",
            "logoid": "infosys"
          },
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NSE:TECHM",
            "logoid": "mahindra-tech"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "TVC:DJI",
            "logoid": "indices/dow-30"
          },
          {
            "symbol": "NSE:HCLTECH",
            "logoid": "hcl-technologies"
          }
        ],
        "storyPath": "/news/moneycontrol:fb0a5811e094b:0-dow-reaches-fresh-high-s-p-500-and-nasdaq-recover-after-higher-than-expected-ppi-data-gift-nifty-up/",
        "provider": {
          "id": "moneycontrol",
          "name": "Moneycontrol",
          "logo_id": "moneycontrol"
        }
      },
      {
        "id": "benzinga:33bba1b36094b:0",
        "title": "Nvidia Rebounds Over 6% After $550B Market Cap Loss",
        "published": 1719348823,
        "urgency": 2,
        "link": "https://www.benzinga.com/top-stories/24/06/39490865/nvidia-rebounds-over-6-after-550b-market-cap-loss",
        "permission": "preview",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:SOX",
            "logoid": "indices/philadelphia-semiconductor-index"
          },
          {
            "symbol": "NASDAQ:QQQ",
            "logoid": "invesco"
          },
          {
            "symbol": "AMEX:IYW",
            "logoid": "ishares"
          },
          {
            "symbol": "AMEX:FTEC",
            "logoid": "fidelity-advantage"
          },
          {
            "symbol": "AMEX:FDN",
            "logoid": "first-trust"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          }
        ],
        "storyPath": "/news/benzinga:33bba1b36094b:0-nvidia-rebounds-over-6-after-550b-market-cap-loss/",
        "provider": {
          "id": "benzinga",
          "name": "Benzinga",
          "logo_id": "benzinga",
          "url": "https://benzinga.com/"
        }
      },
      {
        "id": "moneycontrol:82b05fea0094b:0",
        "title": "Dow closes at a one-month high as investors broaden portfolios",
        "published": 1719276309,
        "urgency": 2,
        "link": "https://www.moneycontrol.com/news/business/markets/dow-closes-at-a-one-month-high-as-investors-broaden-portfolios-12755457.html",
        "relatedSymbols": [
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NYSE:UPS",
            "logoid": "united-parcel"
          },
          {
            "symbol": "TVC:DJI",
            "logoid": "indices/dow-30"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/moneycontrol:82b05fea0094b:0-dow-closes-at-a-one-month-high-as-investors-broaden-portfolios/",
        "provider": {
          "id": "moneycontrol",
          "name": "Moneycontrol",
          "logo_id": "moneycontrol"
        }
      },
      {
        "id": "moneycontrol:20ee689f8094b:0",
        "title": "S&P 500, Nasdaq hit record closing highs ahead of data, Fed comments",
        "published": 1718671630,
        "urgency": 2,
        "link": "https://www.moneycontrol.com/news/business/markets/sp-500-nasdaq-hit-record-closing-highs-ahead-of-data-fed-comments-12750514.html",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:ADSK",
            "logoid": "autodesk"
          },
          {
            "symbol": "NYSE:GS",
            "logoid": "golden-sachs-etf-trust-goldman"
          },
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "NASDAQ:NDAQ",
            "logoid": "nasdaq"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "TWSE:2330",
            "logoid": "taiwan-semiconductor"
          },
          {
            "symbol": "NASDAQ:AVGO",
            "logoid": "broadcom"
          },
          {
            "symbol": "NYSE:EVR",
            "logoid": "evercore-inc"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "TVC:DJI",
            "logoid": "indices/dow-30"
          },
          {
            "symbol": "NASDAQ:MU",
            "logoid": "micron-technology"
          }
        ],
        "storyPath": "/news/moneycontrol:20ee689f8094b:0-s-p-500-nasdaq-hit-record-closing-highs-ahead-of-data-fed-comments/",
        "provider": {
          "id": "moneycontrol",
          "name": "Moneycontrol",
          "logo_id": "moneycontrol"
        }
      },
      {
        "id": "moneycontrol:39bfca96a094b:0",
        "title": "US markets inch up, trade near record highs, S&P 500 up 0.2%; GIFT Nifty flat",
        "published": 1718640974,
        "urgency": 2,
        "link": "https://www.moneycontrol.com/news/business/markets/us-markets-inch-up-trade-near-record-highs-s-gift-nifty-flat-12750450.html",
        "relatedSymbols": [
          {
            "symbol": "NYSE:UNH",
            "logoid": "unitedhealth"
          },
          {
            "symbol": "NYSE:CRM",
            "logoid": "salesforce"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:DIS",
            "logoid": "walt-disney"
          },
          {
            "symbol": "NYSE:MRK",
            "logoid": "merck-and-co"
          }
        ],
        "storyPath": "/news/moneycontrol:39bfca96a094b:0-us-markets-inch-up-trade-near-record-highs-s-p-500-up-0-2-gift-nifty-flat/",
        "provider": {
          "id": "moneycontrol",
          "name": "Moneycontrol",
          "logo_id": "moneycontrol"
        }
      },
      {
        "id": "moneycontrol:0b76c8998094b:0",
        "title": "World Street | Apple beats Microsoft in m-cap, Tesla investors vote for Musk's pay, Gamestop postpones annual meet and more",
        "published": 1718332125,
        "urgency": 2,
        "link": "https://www.moneycontrol.com/news/business/markets/world-street-apple-beats-microsoft-in-m-cap-tesla-investors-greenlight-musks-pay-gamestop-postpones-annual-meet-and-more-12748369.html",
        "relatedSymbols": [
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:ADBE",
            "logoid": "adobe"
          },
          {
            "symbol": "NASDAQ:AVGO",
            "logoid": "broadcom"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/moneycontrol:0b76c8998094b:0-world-street-apple-beats-microsoft-in-m-cap-tesla-investors-vote-for-musk-s-pay-gamestop-postpones-annual-meet-and-more/",
        "provider": {
          "id": "moneycontrol",
          "name": "Moneycontrol",
          "logo_id": "moneycontrol"
        }
      },
      {
        "id": "moneycontrol:7140a1b34094b:0",
        "title": "World Street | Nvidia hits $3-trln mcap, US markets at record high, Foxconn ups guidance and more",
        "published": 1717640178,
        "urgency": 2,
        "link": "https://www.moneycontrol.com/news/business/markets/world-street-nvidia-hits-3-trln-mcap-us-markets-at-record-high-foxconn-ups-guidance-and-more-12742122.html",
        "relatedSymbols": [
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "TWSE:2354",
            "logoid": "foxconn-tech-co"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:BX",
            "logoid": "blackstone"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/moneycontrol:7140a1b34094b:0-world-street-nvidia-hits-3-trln-mcap-us-markets-at-record-high-foxconn-ups-guidance-and-more/",
        "provider": {
          "id": "moneycontrol",
          "name": "Moneycontrol",
          "logo_id": "moneycontrol"
        }
      },
      {
        "id": "moneycontrol:dd1b5e6e7094b:0",
        "title": "US markets up as rate cut expectations revive, S&P trades 0.65% higher; GIFT Nifty down",
        "published": 1715011456,
        "urgency": 2,
        "link": "https://www.moneycontrol.com/news/business/markets/us-markets-up-as-rate-cut-expectations-revive-s-gift-nifty-down-12715923.html",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/moneycontrol:dd1b5e6e7094b:0-us-markets-up-as-rate-cut-expectations-revive-s-p-trades-0-65-higher-gift-nifty-down/",
        "provider": {
          "id": "moneycontrol",
          "name": "Moneycontrol",
          "logo_id": "moneycontrol"
        }
      },
      {
        "id": "moneycontrol:231dc6f6f094b:0",
        "title": "From gloom to glory: How the market’s giant wheel turned in 2023",
        "published": 1705728240,
        "urgency": 2,
        "link": "https://www.moneycontrol.com/news/opinion/from-gloom-to-glory-how-the-markets-giant-wheel-turned-in-2023-12089701.html",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          }
        ],
        "storyPath": "/news/moneycontrol:231dc6f6f094b:0-from-gloom-to-glory-how-the-market-s-giant-wheel-turned-in-2023/",
        "provider": {
          "id": "moneycontrol",
          "name": "Moneycontrol",
          "logo_id": "moneycontrol"
        }
      },
      {
        "id": "moneycontrol:6ac392994094b:0",
        "title": "S&P 500 ends near record high as AI optimism lifts chipmakers",
        "published": 1705625549,
        "urgency": 2,
        "link": "https://www.moneycontrol.com/news/business/markets/sp-500-ends-near-record-high-as-ai-optimism-lifts-chipmakers-12081151.html",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "TWSE:2330",
            "logoid": "taiwan-semiconductor"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/moneycontrol:6ac392994094b:0-s-p-500-ends-near-record-high-as-ai-optimism-lifts-chipmakers/",
        "provider": {
          "id": "moneycontrol",
          "name": "Moneycontrol",
          "logo_id": "moneycontrol"
        }
      },
      {
        "id": "moneycontrol:e25aece1a094b:0",
        "title": "S&P 500 slips, after rising briefly above record close, on CPI data",
        "published": 1704991554,
        "urgency": 2,
        "link": "https://www.moneycontrol.com/news/business/markets/sp-500-slips-after-rising-briefly-above-record-close-on-cpi-data-12037341.html",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:COIN",
            "logoid": "coinbase"
          },
          {
            "symbol": "NYSE:WFC",
            "logoid": "wells-fargo"
          },
          {
            "symbol": "LSE:STAN",
            "logoid": "standard-chartered"
          },
          {
            "symbol": "NYSE:BAC",
            "logoid": "bank-of-america"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "TVC:DJI",
            "logoid": "indices/dow-30"
          },
          {
            "symbol": "NYSE:C",
            "logoid": "citigroup"
          },
          {
            "symbol": "NYSE:JPM",
            "logoid": "jpmorgan-chase"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/moneycontrol:e25aece1a094b:0-s-p-500-slips-after-rising-briefly-above-record-close-on-cpi-data/",
        "provider": {
          "id": "moneycontrol",
          "name": "Moneycontrol",
          "logo_id": "moneycontrol"
        }
      },
      {
        "id": "moneycontrol:b24f5d2ac094b:0",
        "title": "US stocks see further weakness after buoyant 2023",
        "published": 1704294185,
        "urgency": 2,
        "link": "https://www.moneycontrol.com/news/business/markets/us-stocks-see-further-weakness-after-buoyant-2023-11994701.html",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "TVC:DJI",
            "logoid": "indices/dow-30"
          }
        ],
        "storyPath": "/news/moneycontrol:b24f5d2ac094b:0-us-stocks-see-further-weakness-after-buoyant-2023/",
        "provider": {
          "id": "moneycontrol",
          "name": "Moneycontrol",
          "logo_id": "moneycontrol"
        }
      },
      {
        "id": "moneycontrol:5304c99ff094b:0",
        "title": "US stocks slip to start the new year",
        "published": 1704210998,
        "urgency": 2,
        "link": "https://www.moneycontrol.com/news/business/us-stocks-slip-to-start-the-new-year-11989761.html",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          }
        ],
        "storyPath": "/news/moneycontrol:5304c99ff094b:0-us-stocks-slip-to-start-the-new-year/",
        "provider": {
          "id": "moneycontrol",
          "name": "Moneycontrol",
          "logo_id": "moneycontrol"
        }
      },
      {
        "id": "leverage_shares:4dab16e9d094b:0",
        "title": "“Magnificent 7” deflates",
        "published": 1698856103,
        "urgency": 2,
        "link": "https://leverageshares.com/en/insights/magnificent-7-deflates/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "LSE:3AME",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3APE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SALE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SPY3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:3MSE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:1BRN",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:TSLA",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:5SPY",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3GOE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3SMT",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:GOO1",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3SMZ",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:3TSE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:NVI3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:STSE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SAPE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:SPL",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:2FB",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:SMF3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AMZN",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SSPE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:3APE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:3SAA",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:GG3S",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:TSLQ",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SP5Y",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3SYE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:GOOE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:2AAP",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:NV3S",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3NVE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAPS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAP3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:2TSL",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3SAA",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAP2",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAPE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3FBE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3TSL",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AM3S",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:NVDS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:TSL2",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:NVD2",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:MSF1",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AMZ3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:1STS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:GOO3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:NVIS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:TS3S",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SFB3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SSPY",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3GOO",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3MSF",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:1NDA",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:TS3S",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:2MSF",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3AMZ",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3SAM",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:FB1"
          },
          {
            "symbol": "XETR:FB3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:SSPY",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:1AAP"
          },
          {
            "symbol": "LSE:3TSE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:TSL1",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3SMF",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:3AN",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:GOOG",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:MSFS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "BMV:TS3S/N"
          },
          {
            "symbol": "LSE:SNVE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:2NVD",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:TS2S",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:1AMZ",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:GG3S",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:KRON"
          },
          {
            "symbol": "LSE:3AAP",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:FB2E",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:APLS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SNDE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:3GGL",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:FBE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:MS3S",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SMSF",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:MSSE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:MSFT",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:2STE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:TSLS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:1GOO",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:NVD3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAP1"
          },
          {
            "symbol": "LSE:GGES",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3FB",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:FB3S",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:GOOS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:2STS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3MSE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:MSF2",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SNV3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:2TSE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:5SPE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:STSL",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3NVD",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:FB2",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:GOOE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:NVDE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SGOO",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:1APS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AMZ1",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:FB1X"
          },
          {
            "symbol": "LSE:MSFE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AMZE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:2AMZ",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SGOE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SNVD",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:FB3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SAPL",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:GOO2",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SPYS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:1TSL",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:FB3S",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:MSF3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:1FB"
          },
          {
            "symbol": "LSE:3SGG",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:TSL3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:5SPE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:2GOO",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3STL",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:1MSF",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:3SAM",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3SPY",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AMZ2",
            "logoid": "leverage-shares"
          }
        ],
        "storyPath": "/news/leverage_shares:4dab16e9d094b:0-magnificent-7-deflates/",
        "provider": {
          "id": "leverage_shares",
          "name": "Leverage Shares",
          "logo_id": "leverage-shares",
          "url": "https://leverageshares.com/en/"
        }
      },
      {
        "id": "leverage_shares:c32a25477094b:0",
        "title": "Big 7 vs Reality",
        "published": 1697722256,
        "urgency": 2,
        "link": "https://leverageshares.com/en/insights/big-7-vs-reality/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "LSE:3MSF",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:1BRN",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3SMF",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:NVD3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3SGG",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:GOOE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SPYS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:TS3S",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:SMF3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:1APS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:1NDA",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:3AN",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:NVD2",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AMZ1",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:NVDE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:TSLQ",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SALE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:GOO2",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:GOOE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:TS2S",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:SSPY",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3GOE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "BMV:TS3S/N"
          },
          {
            "symbol": "XETR:3GGL",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3AAP",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3SYE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SP5Y",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:NVI3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AMZN",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3TSL",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3STL",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:3TSE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3SMZ",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:STSL",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:3SAM",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AMZ3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:MS3S",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:2TSL",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:1MSF",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:2STE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAPE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:MSF3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:GG3S",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAPS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SSPE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:1GOO",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3SMT",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:SPL",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3MSE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3SPY",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:MSFS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:APLS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:GOOS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SNDE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:TSL3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:2TSE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3APE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AMZ2",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3NVE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:2AAP",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:2GOO",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:MSFT",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:1STS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:GG3S",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:GOO1",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:GOO3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SAPL",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:2AMZ",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:STSE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3NVD",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:GGES",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3AMZ",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SSPY",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3AME",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:TSL2",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:1TSL",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:TSL1",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SGOE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:2STS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAP1"
          },
          {
            "symbol": "LSE:SMSF",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:TSLS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3SAA",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:MSSE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:MSF1",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AM3S",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:MSFE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SPY3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:3APE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:3MSE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:KRON"
          },
          {
            "symbol": "LSE:MSF2",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:2MSF",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SNVD",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SNVE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3TSE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:5SPE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:5SPY",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAP3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:GOOG",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:NVIS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAP2",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:NV3S",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3GOO",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:3SAA",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:TS3S",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AMZE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SGOO",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:NVDS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SNV3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:2NVD",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:TSLA",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:1AAP"
          },
          {
            "symbol": "LSE:3SAM",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SAPE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:5SPE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:1AMZ",
            "logoid": "leverage-shares"
          }
        ],
        "storyPath": "/news/leverage_shares:c32a25477094b:0-big-7-vs-reality/",
        "provider": {
          "id": "leverage_shares",
          "name": "Leverage Shares",
          "logo_id": "leverage-shares",
          "url": "https://leverageshares.com/en/"
        }
      },
      {
        "id": "leverage_shares:48fb3b495094b:0",
        "title": "2 Markets 2 Different Tales",
        "published": 1697126697,
        "urgency": 2,
        "link": "https://leverageshares.com/en/insights/2-markets-2-different-tales/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:COIN",
            "logoid": "coinbase"
          },
          {
            "symbol": "LSE:5TLT",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SP5Y",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:TLT5",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:MRNA",
            "logoid": "moderna"
          },
          {
            "symbol": "LSE:SPY3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:TL5S",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SPYS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "NASDAQ:SQQQ",
            "logoid": "proshares"
          },
          {
            "symbol": "XETR:SPL",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "NASDAQ:QQQ",
            "logoid": "invesco"
          },
          {
            "symbol": "LSE:TLT5",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "NASDAQ:TQQQ",
            "logoid": "proshares"
          },
          {
            "symbol": "LSE:SSPE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:5STL",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:KRON"
          },
          {
            "symbol": "XETR:5SPE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3SYE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SSPY",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3SPY",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:5STL",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:5SPE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:SSPY",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:5SPY",
            "logoid": "leverage-shares"
          }
        ],
        "storyPath": "/news/leverage_shares:48fb3b495094b:0-2-markets-2-different-tales/",
        "provider": {
          "id": "leverage_shares",
          "name": "Leverage Shares",
          "logo_id": "leverage-shares",
          "url": "https://leverageshares.com/en/"
        }
      },
      {
        "id": "leverage_shares:cdaefb068094b:0",
        "title": "Inflation Trends and Monetary Policy",
        "published": 1691684312,
        "urgency": 2,
        "link": "https://leverageshares.com/en/insights/inflation-trends-and-monetary-policy/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:COIN",
            "logoid": "coinbase"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:SQQQ",
            "logoid": "proshares"
          },
          {
            "symbol": "NASDAQ:MRNA",
            "logoid": "moderna"
          },
          {
            "symbol": "NASDAQ:QQQ",
            "logoid": "invesco"
          },
          {
            "symbol": "NASDAQ:TQQQ",
            "logoid": "proshares"
          },
          {
            "symbol": "LSE:5QQE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:QQ3S",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3QQQ",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:QQQ5",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:QQ3S",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SQQQ",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:QQQ5",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3QQE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SQQE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:5QQQ",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:QQL3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:QQL3",
            "logoid": "leverage-shares"
          }
        ],
        "storyPath": "/news/leverage_shares:cdaefb068094b:0-inflation-trends-and-monetary-policy/",
        "provider": {
          "id": "leverage_shares",
          "name": "Leverage Shares",
          "logo_id": "leverage-shares",
          "url": "https://leverageshares.com/en/"
        }
      },
      {
        "id": "leverage_shares:4e228217d094b:0",
        "title": "German Equities Remain Under Pressure",
        "published": 1691583351,
        "urgency": 2,
        "link": "https://leverageshares.com/en/insights/german-equities-remain-under-pressure/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "LSE:3XEE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "NASDAQ:QQQ",
            "logoid": "invesco"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:COIN",
            "logoid": "coinbase"
          },
          {
            "symbol": "XETR:3XEE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "NASDAQ:MRNA",
            "logoid": "moderna"
          },
          {
            "symbol": "NASDAQ:TQQQ",
            "logoid": "proshares"
          },
          {
            "symbol": "LSE:3SEE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "NASDAQ:SQQQ",
            "logoid": "proshares"
          },
          {
            "symbol": "LSE:XLE3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3XLE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:SXLG"
          },
          {
            "symbol": "LSE:XLGS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SXLG",
            "logoid": "leverage-shares"
          }
        ],
        "storyPath": "/news/leverage_shares:4e228217d094b:0-german-equities-remain-under-pressure/",
        "provider": {
          "id": "leverage_shares",
          "name": "Leverage Shares",
          "logo_id": "leverage-shares",
          "url": "https://leverageshares.com/en/"
        }
      },
      {
        "id": "leverage_shares:016aaf033094b:0",
        "title": "The magnificent seven",
        "published": 1687272754,
        "urgency": 2,
        "link": "https://leverageshares.com/en/insights/the-magnificent-seven/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "XETR:1NDA",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3FBE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:1BRN",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:FB1"
          },
          {
            "symbol": "LSE:5SPY",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:FB2",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAP3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SSPE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:SSPY",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:3APE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3NVD",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3APE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:1APS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:3SAA",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAP1"
          },
          {
            "symbol": "LSE:SPYS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SAPL",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:5SPE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AMZ1",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SSPY",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SALE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:FB3S",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AMZE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3SAA",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3SMZ",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAPS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:1FB"
          },
          {
            "symbol": "XETR:SPL",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:3SAM",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:NVDE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:3AN",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3FB",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:FB2E",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SNVD",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3AME",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AMZN",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:NV3S",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:KRON"
          },
          {
            "symbol": "LSE:SNVE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:5SPE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3NVE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3SAM",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:APLS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SP5Y",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAP2",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:2AMZ",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:FBE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3SPY",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:FB3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:NVD2",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3AMZ",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3SYE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SAPE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAPE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SNV3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:2AAP",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:NVI3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:FB3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:FB1X"
          },
          {
            "symbol": "XETR:NVIS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:NVD3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:FB3S",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:1AAP"
          },
          {
            "symbol": "LSE:SFB3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AMZ3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SPY3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:1AMZ",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3AAP",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AMZ2",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:NVDS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:2NVD",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AM3S",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SNDE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:2FB",
            "logoid": "leverage-shares"
          }
        ],
        "storyPath": "/news/leverage_shares:016aaf033094b:0-the-magnificent-seven/",
        "provider": {
          "id": "leverage_shares",
          "name": "Leverage Shares",
          "logo_id": "leverage-shares",
          "url": "https://leverageshares.com/en/"
        }
      },
      {
        "id": "leverage_shares:2e368ace2094b:0",
        "title": "S&P 500 enters bull market",
        "published": 1686584821,
        "urgency": 2,
        "link": "https://leverageshares.com/en/insights/sp-500-enters-bull-market/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "LSE:1BRN",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:5SPE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3QQQ",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SQQE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:QQ3S",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SSPY",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3SPY",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3SYE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3AAP",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SPYS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "NASDAQ:SQQQ",
            "logoid": "proshares"
          },
          {
            "symbol": "LSE:AAP1"
          },
          {
            "symbol": "LSE:QQQ5",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SSPE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:5SPY",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SP5Y",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:QQL3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:2AAP",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:1AAP"
          },
          {
            "symbol": "LSE:SPY3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SQQQ",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAP2",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3APE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAPE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:3APE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:5QQQ",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:5QQE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAP3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3QQE",
            "logoid": "leverage-shares"
          }
        ],
        "storyPath": "/news/leverage_shares:2e368ace2094b:0-s-p-500-enters-bull-market/",
        "provider": {
          "id": "leverage_shares",
          "name": "Leverage Shares",
          "logo_id": "leverage-shares",
          "url": "https://leverageshares.com/en/"
        }
      },
      {
        "id": "leverage_shares:5763ac7d0094b:0",
        "title": "Bonds vs Equities and the Debt Deal: Is a Winter Coming?",
        "published": 1686031200,
        "urgency": 2,
        "link": "https://leverageshares.com/en/insights/bonds-vs-equities-and-the-debt-deal-is-a-winter-coming/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:QQQ",
            "logoid": "invesco"
          },
          {
            "symbol": "LSE:1BRN",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "NASDAQ:TQQQ",
            "logoid": "proshares"
          },
          {
            "symbol": "NASDAQ:SQQQ",
            "logoid": "proshares"
          },
          {
            "symbol": "XETR:3APE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAPE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:2AAP",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3APE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3AAP",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAP1"
          },
          {
            "symbol": "LSE:AAP2",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:1AAP"
          },
          {
            "symbol": "LSE:AAP3",
            "logoid": "leverage-shares"
          }
        ],
        "storyPath": "/news/leverage_shares:5763ac7d0094b:0-bonds-vs-equities-and-the-debt-deal-is-a-winter-coming/",
        "provider": {
          "id": "leverage_shares",
          "name": "Leverage Shares",
          "logo_id": "leverage-shares",
          "url": "https://leverageshares.com/en/"
        }
      },
      {
        "id": "leverage_shares:db779eb35094b:0",
        "title": "Markets Retreat as Debt-Ceiling Deadline Looms",
        "published": 1685018138,
        "urgency": 2,
        "link": "https://leverageshares.com/en/insights/markets-retreat-as-debt-ceiling-deadline-looms/",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "LSE:1BRN",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3ABE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3APE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SAPL",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAP2",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:1APS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAPS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SSPE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:COI1",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:1AAP"
          },
          {
            "symbol": "LSE:SSPY",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SPYS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:3SAA",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SAPE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:COIB",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AMZ3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:ABN3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAP1"
          },
          {
            "symbol": "LSE:FB3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:2AAP",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3AAP",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3CNE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:S3CO",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3SAA",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SPY3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAP3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:ABN3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:3APE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3ABN",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:CON3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:GOO3",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:1COI",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:SALE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "XETR:3COI",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:AAPE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3CON",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3SPY",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:3SYE",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:APLS",
            "logoid": "leverage-shares"
          },
          {
            "symbol": "LSE:CO3S",
            "logoid": "leverage-shares"
          }
        ],
        "storyPath": "/news/leverage_shares:db779eb35094b:0-markets-retreat-as-debt-ceiling-deadline-looms/",
        "provider": {
          "id": "leverage_shares",
          "name": "Leverage Shares",
          "logo_id": "leverage-shares",
          "url": "https://leverageshares.com/en/"
        }
      }
    ],
    "streaming": {
      "channel": "f2ed8d1af7cc2ff3c73125e1153b"
    }
  },
  "msg": "Success"
}
```

## Get Stock News

`GET /api/news/stock`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/api/news/stock?symbol=NASDAQ%3AAAPL&lang=en&market_country=US' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "tag:reuters.com,2026:newsml_L1N41401E:0",
        "title": "Apple's new CEO is a product perfectionist taking on the AI age",
        "published": 1776765600,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L1N41401E:0-apple-s-new-ceo-is-a-product-perfectionist-taking-on-the-ai-age/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260421001775:0",
        "title": "Tim Cook Told Me His Advice for Apple's Next CEO — WSJ",
        "published": 1776763800,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260421001775:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260421001551:0",
        "title": "How Apple Stock Has Fared Under Tim Cook — WSJ",
        "published": 1776761940,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260421001551:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260421001485:0",
        "title": "Apple AI Ambitions Helped by Incoming CEO's Hardware Experience — Market Talk",
        "published": 1776760800,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260421001485:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:9cafd3a72094b:0",
        "title": "Nasdaq, S&P 500 Futures Steady As Iran Talks, Warsh Hearing Set Market Tone: Why AAPL, AMZN, POET, FRMI, IBRX Are In Focus",
        "published": 1776760781,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/nasdaq-sp500-futures-rise-aapl-amzn-poet-frmi-ibrx-stocks-to-watch/cZBIfgmRICh",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "BCBA:SPY",
            "logoid": "spdr-sandp500-etf-tr"
          }
        ],
        "storyPath": "/news/stocktwits:9cafd3a72094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_DN20260420009243:0",
        "title": "Apple CEO Cook Plans His Departure. The Tech Giant He Leaves Behind Won't Be the Same. — Barrons.com",
        "published": 1776759180,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260420009243:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:5692ebe19094b:0",
        "title": "Apple's New CEO Led A Silicon 'Brain Transplant' — Analyst Says That's Exactly Why John Ternus Is Right For Next AI Phase",
        "published": 1776757050,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-s-new-ceo-led-a-silicon-brain-transplant-analyst-says-that-s-exactly-why-john-ternus-is-right-for-next-ai-phase/cZBI9pwRICa",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:5692ebe19094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "tradingview:d76fed67f094b:0",
        "title": "AAPL: Apple Stock Tumbles as CEO Tim Cook Announces Departure After 15 Years",
        "published": 1776755710,
        "urgency": 2,
        "link": "https://www.tradingview.com",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/tradingview:d76fed67f094b:0-aapl-apple-stock-tumbles-as-ceo-tim-cook-announces-departure-after-15-years/",
        "provider": {
          "id": "tradingview",
          "name": "TradingView",
          "logo_id": "tradingview-snaps"
        }
      },
      {
        "id": "sharecast:674e9b6e8094b:0",
        "title": " Apple names John Ternus as CEO to replace Tim Cook ",
        "published": 1776753179,
        "urgency": 2,
        "link": "https://www.sharecast.com/news/news-and-announcements/apple-names-john-ternus-as-ceo-to-replace-tim-cook--22320629.html",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/sharecast:674e9b6e8094b:0/",
        "provider": {
          "id": "sharecast",
          "name": "ShareCast",
          "logo_id": "sharecast"
        }
      },
      {
        "id": "stocktwits:99c909d7b094b:0",
        "title": "Apple After Tim Cook: Analysts See Continuity Pick, Not Vision Play Under New CEO John Ternus",
        "published": 1776740903,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-after-tim-cook-analysts-see-continuity-pick-not-vision-play-under-new-ceo-john-ternus/cZBIPluRIzz",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:99c909d7b094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_DN20260420009691:0",
        "title": "The Rise of Apple's New CEO: A Hardware Expert Takes Over in the AI Era — WSJ",
        "published": 1776739500,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260420009691:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L6N41400X:0",
        "title": "Apple CEO’s best bet: channel both Jobs and Cook",
        "published": 1776733042,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L6N41400X:0-apple-ceo-s-best-bet-channel-both-jobs-and-cook/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_SN20260420010143:0",
        "title": "Apple CEO Tim Cook to step down after overseeing 1,900% stock surge. His successor faces big challenges.",
        "published": 1776732180,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_SN20260420010143:0/",
        "provider": {
          "id": "market-watch",
          "name": "MarketWatch",
          "logo_id": "marketwatch"
        }
      },
      {
        "id": "DJN_DN20260420008139:0",
        "title": "Tim Cook to Step Down as Apple Names New CEO — WSJ",
        "published": 1776730980,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260420008139:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "dpa_afx:d24ca8bee7549:0",
        "title": "Apple Names John Ternus CEO; Tim Cook To Become Executive Chairman",
        "published": 1776723693,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/dpa_afx:d24ca8bee7549:0-apple-names-john-ternus-ceo-tim-cook-to-become-executive-chairman/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L4N4131HC:0",
        "title": "Who is John Ternus, Apple's new CEO?",
        "published": 1776721816,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L4N4131HC:0-who-is-john-ternus-apple-s-new-ceo/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260420008672:0",
        "title": "Apple's New CEO Will Face Immediate Pressure on AI Strategy — Market Talk",
        "published": 1776721080,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260420008672:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tradingview:9a9b700e6fc12:0",
        "title": "Apple's Tim Cook to Become Executive Chair; John Ternus Named CEO",
        "published": 1776720780,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/tradingview:9a9b700e6fc12:0-apple-s-tim-cook-to-become-executive-chair-john-ternus-named-ceo/",
        "provider": {
          "id": "tradingview",
          "name": "TradingView",
          "logo_id": "tradingview-snaps"
        }
      },
      {
        "id": "DJN_DN20260420008527:0",
        "title": "Apple's CEO Change Timing Will Garner Mixed Reaction, Analyst Says — Market Talk",
        "published": 1776720240,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260420008527:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260420008407:0",
        "title": "Apple Stock Down After-Hours After John Ternus Named Next CEO — WSJ",
        "published": 1776719280,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260420008407:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260420008355:0",
        "title": "Apple Picks Exec With Core Hardware Expertise as Next CEO — Market Talk",
        "published": 1776719040,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260420008355:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260420008272:0",
        "title": "Apple's Cook to Continue to Engage With Global Policymakers — Market Talk",
        "published": 1776718620,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260420008272:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:0acb0ab69094b:0",
        "title": "Apple Appoints New CEO; Tim Cook Shifts To Executive Chairman",
        "published": 1776718532,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-appoints-new-ceo-tim-cook-shifts-to-executive-chairman/cZBdnvoRIzq",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:0acb0ab69094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_DN20260420008241:0",
        "title": "Apple's Ends Months of Speculation Over Tim Cook's Successor — Market Talk",
        "published": 1776718500,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260420008241:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L4N4131GO:0",
        "title": "Apple turns to hardware veteran Ternus as CEO to succeed Cook in AI age",
        "published": 1776717647,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L4N4131GO:0-apple-turns-to-hardware-veteran-ternus-as-ceo-to-succeed-cook-in-ai-age/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN4130WL:0",
        "title": "Johny Srouji Named Apple’s Chief Hardware Officer",
        "published": 1776717291,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN4130WL:0-johny-srouji-named-apple-s-chief-hardware-officer/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L4N4131GB:0",
        "title": "John Ternus to become Apple CEO, Tim Cook to become executive chairman",
        "published": 1776717225,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L4N4131GB:0-john-ternus-to-become-apple-ceo-tim-cook-to-become-executive-chairman/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260420007764_20260420007925:0",
        "title": "Apple: Ternus Will Join the Bd of Directors, Also Effective Sept 1 >AAPL",
        "published": 1776717180,
        "urgency": 1,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260420007764_20260420007925:0/",
        "is_flash": true,
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260420007764_20260420007885:0",
        "title": "Apple: Transition, Which Was Approved Unanimously by the Bd of Directors, Follows a Thoughtful, Long-Term Succession Planning Process >AAPL",
        "published": 1776717060,
        "urgency": 1,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260420007764_20260420007885:0/",
        "is_flash": true,
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260420007788_20260420007857:0",
        "title": "Apple: Johny Srouji Will Become Chief Hardware Officer, Effective Immediately >AAPL",
        "published": 1776717000,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260420007788_20260420007857:0/",
        "is_flash": true,
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260420006199:0",
        "title": "Apple Stock Can Hit $300 Despite Memory Headwinds, Analyst Says. Here's How. — Barrons.com",
        "published": 1776703320,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260420006199:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260418000740:0",
        "title": "Berkshire May Have Sold $15 Billion of Stocks Run by Former Manager — Barrons.com",
        "published": 1776527760,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NYSE:AXP",
            "logoid": "american-express"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:BRK.A",
            "logoid": "berkshire-hathaway"
          },
          {
            "symbol": "NYSE:COF",
            "logoid": "capital-one"
          },
          {
            "symbol": "NYSE:OXY",
            "logoid": "occidental-petroleum"
          }
        ],
        "storyPath": "/news/DJN_DN20260418000740:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:5dd968a69094b:0",
        "title": "Apple Clears Major Legal Hurdle After US Trade Tribunal Shuts Down Masimo’s Latest Watch Ban Attempt",
        "published": 1776472317,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-clears-major-legal-hurdle-after-us-trade-tribunal-shuts-down-masimos-latest-watch-ban-attempt/cZJ6WUSRIUr",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:5dd968a69094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L6N4101BB:0",
        "title": "Apple defeats bid for new Apple Watch import ban at US trade tribunal ",
        "published": 1776467696,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MASI",
            "logoid": "masimo"
          },
          {
            "symbol": "NYSE:DHR",
            "logoid": "danaher"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L6N4101BB:0-apple-defeats-bid-for-new-apple-watch-import-ban-at-us-trade-tribunal/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260417004938:0",
        "title": "Apple Seen Poised to Gain Smartphone Market Share — Market Talk",
        "published": 1776441060,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260417004938:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:abfd331bf094b:0",
        "title": "Apple’s China Surge Shows Pricing Power Matters In A Supply Crunch – Retail Bulls Take Notice",
        "published": 1776435624,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-china-surge-shows-pricing-power-matters-in-a-supply-crunch-retail-bulls-take-notice/cZJUsxBRIUG",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:abfd331bf094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_DN20260417004032:0",
        "title": "Apple Raised to Outperform From Neutral by BNP Paribas",
        "published": 1776434400,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260417004032:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L1N41008E:0",
        "title": "Apple's iPhone shipments in China surge 20% in Q1, data shows",
        "published": 1776414427,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "HKEX:1810",
            "logoid": "xiaomi"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L1N41008E:0-apple-s-iphone-shipments-in-china-surge-20-in-q1-data-shows/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L4N4100B5:0",
        "title": "Apple marketing chief for watch, AirPods, home and health Stan Ng retires - Bloomberg News",
        "published": 1776401681,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L4N4100B5:0-apple-marketing-chief-for-watch-airpods-home-and-health-stan-ng-retires-bloomberg-news/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260416008149:0",
        "title": "TSMC's Results Weren't a Great Sign for Apple — Heard on the Street — WSJ",
        "published": 1776366900,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "TWSE:2330",
            "logoid": "taiwan-semiconductor"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "isExclusive": true,
        "storyPath": "/news/DJN_DN20260416008149:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260415008637:0",
        "title": "Former Apple Exec Leaves Ford in Tech Reorganization — Barrons.com",
        "published": 1776290160,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:F",
            "logoid": "ford"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          }
        ],
        "storyPath": "/news/DJN_DN20260415008637:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260415008356:0",
        "title": "The S&P 500 Just Surged to a Record High Despite a War. Why It May Keep Rising. — Barrons.com",
        "published": 1776286620,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "CBOE:SPX",
            "logoid": "indices/s-and-p-500"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          }
        ],
        "storyPath": "/news/DJN_DN20260415008356:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stockstory:7cf1a340f094b:0",
        "title": "Apple (AAPL) Stock Trades Up, Here Is Why",
        "published": 1776281751,
        "urgency": 2,
        "link": "https://stockstory.org/us/stocks/nasdaq/aapl/news/why-up-down/apple-aapl-stock-trades-up-here-is-why-4",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stockstory:7cf1a340f094b:0-apple-aapl-stock-trades-up-here-is-why/",
        "provider": {
          "id": "stockstory",
          "name": "Stock Story",
          "logo_id": "stockstory",
          "url": "https://stockstory.org/"
        }
      },
      {
        "id": "DJN_DN20260414007032:0",
        "title": "Apple and Amazon Partner on Satellite Deal. Why It Makes Sense. — Barrons.com",
        "published": 1776193740,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260414007032:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260414002395:0",
        "title": "Apple Is Maintained at Buy by B of A Securities",
        "published": 1776163380,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260414002395:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260410001611:0",
        "title": "Tech Trader: Apple Fell Behind With Gen-Z. The Neo Changed Everything. — Barron's",
        "published": 1775871000,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260410001611:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "dpa_afx:79a707a53529f:0",
        "title": "Apple To Shut Down 3 Retail Stores, Including First Unionized Outlet In Towson",
        "published": 1775844789,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/dpa_afx:79a707a53529f:0-apple-to-shut-down-3-retail-stores-including-first-unionized-outlet-in-towson/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "DJN_DN20260410003674:0",
        "title": "Anthropic Has Banks, Regulators Rattled Over AI Cyber Risks. Some Big Names Could Benefit. — Barrons.com",
        "published": 1775822820,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:CRWD",
            "logoid": "crowdstrike"
          },
          {
            "symbol": "NYSE:JPM",
            "logoid": "jpmorgan-chase"
          },
          {
            "symbol": "NASDAQ:PANW",
            "logoid": "palo-alto-networks"
          }
        ],
        "storyPath": "/news/DJN_DN20260410003674:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:eaf71f338094b:0",
        "title": "Apple Outperforms In Tough Q1 Even As Memory Crunch Drags Global Smartphone Shipments",
        "published": 1775820020,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-outperforms-in-tough-q1-even-as-memory-crunch-drags-global-smartphone-shipments/cZJ0a2PRIte",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:eaf71f338094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN40S1DJ:0",
        "title": "Later This Month, Apple TV To Be Available Via Prime Video In The U.S. As An Add-On Subscription For $9.99 Per Month",
        "published": 1775817039,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN40S1DJ:0-later-this-month-apple-tv-to-be-available-via-prime-video-in-the-u-s-as-an-add-on-subscription-for-9-99-per-month/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L4N40T0PA:0",
        "title": "Apple leads smartphone market even as overall shipments decline, Counterpoint says",
        "published": 1775815508,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "KRX:005930",
            "logoid": "samsung"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L4N40T0PA:0-apple-leads-smartphone-market-even-as-overall-shipments-decline-counterpoint-says/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L1N40T08B:0",
        "title": "Apple leads global smartphone shipments in first quarter, Counterpoint says",
        "published": 1775811689,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L1N40T08B:0-apple-leads-global-smartphone-shipments-in-first-quarter-counterpoint-says/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260409006711:0",
        "title": "Amazon Stock Jumps on DOJ's NFL Probe. It's About 'Affordability for Consumers.' — Barrons.com",
        "published": 1775766360,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NFLX",
            "logoid": "netflix"
          },
          {
            "symbol": "NASDAQ:PSKY",
            "logoid": "viacomcbs"
          }
        ],
        "storyPath": "/news/DJN_DN20260409006711:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_SN20260409009895:0",
        "title": "Big Tech stocks look like especially good deals as investors eye what is next for the market",
        "published": 1775748840,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:PLTR",
            "logoid": "palantir"
          }
        ],
        "storyPath": "/news/DJN_SN20260409009895:0/",
        "provider": {
          "id": "market-watch",
          "name": "MarketWatch",
          "logo_id": "marketwatch"
        }
      },
      {
        "id": "DJN_DN20260408006647:0",
        "title": "How Wall Street Went from Iran War Angst to Watching for a New S&P 500 Record — Barrons.com",
        "published": 1775667540,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "CBOE:SPX",
            "logoid": "indices/s-and-p-500"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NYSE:JPM",
            "logoid": "jpmorgan-chase"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          }
        ],
        "storyPath": "/news/DJN_DN20260408006647:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260408001215:0",
        "title": "Warren Buffett Is Retired. His Latest Advice Couldn't Be More Timely for Young Investors. — Barrons.com",
        "published": 1775629800,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:BRK.A",
            "logoid": "berkshire-hathaway"
          }
        ],
        "storyPath": "/news/DJN_DN20260408001215:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_SN20260407011240:0",
        "title": "Apple's stock pares losses. Here's how to think about the latest saga with foldable iPhones.",
        "published": 1775597460,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_SN20260407011240:0/",
        "provider": {
          "id": "market-watch",
          "name": "MarketWatch",
          "logo_id": "marketwatch"
        }
      },
      {
        "id": "DJN_DN20260407006693:0",
        "title": "Palo Alto, CrowdStrike Stocks Pop After Anthropic Announces Partnerships — Barrons.com",
        "published": 1775592540,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AVGO",
            "logoid": "broadcom"
          },
          {
            "symbol": "NASDAQ:CSCO",
            "logoid": "cisco"
          },
          {
            "symbol": "NASDAQ:CRWD",
            "logoid": "crowdstrike"
          },
          {
            "symbol": "NYSE:JPM",
            "logoid": "jpmorgan-chase"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:PANW",
            "logoid": "palo-alto-networks"
          }
        ],
        "storyPath": "/news/DJN_DN20260407006693:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN40Q02L:0",
        "title": "Apple’s Foldable iPhone Remains On Track For September Debut - Bloomberg News",
        "published": 1775581554,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN40Q02L:0-apple-s-foldable-iphone-remains-on-track-for-september-debut-bloomberg-news/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "stocktwits:3f6b9040a094b:0",
        "title": "AAPL Stock Slides As iPhone-Maker Faces Modest App Store Growth In Q1 – Retail Says ‘Great Opportunity’ To Buy More",
        "published": 1775580095,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/aapl-stock-slides-as-i-phone-maker-faces-modest-app-store-growth-in-q1-retail-says-great-opportunity-to-buy-more/cZJJUImRIpw",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:3f6b9040a094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_DN20260407005480:0",
        "title": "Apple Stock Drops on Foldable iPhone Delay Fears — Barrons.com",
        "published": 1775579460,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260407005480:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stockstory:df3b03abe094b:0",
        "title": "Why Apple (AAPL) Shares Are Falling Today",
        "published": 1775579443,
        "urgency": 2,
        "link": "https://stockstory.org/us/stocks/nasdaq/aapl/news/why-up-down/why-apple-aapl-shares-are-falling-today-3",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stockstory:df3b03abe094b:0-why-apple-aapl-shares-are-falling-today/",
        "provider": {
          "id": "stockstory",
          "name": "Stock Story",
          "logo_id": "stockstory",
          "url": "https://stockstory.org/"
        }
      },
      {
        "id": "DJN_DN20260407004720:0",
        "title": "Apple Shares Fall on Report of Foldable iPhone Engineering Setbacks",
        "published": 1775574720,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260407004720:0-apple-shares-fall-on-report-of-foldable-iphone-engineering-setbacks/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260407004477:0",
        "title": "Apple Stock Drags Down the Dow — WSJ",
        "published": 1775572500,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "TVC:DJI",
            "logoid": "indices/dow-30"
          }
        ],
        "storyPath": "/news/DJN_DN20260407004477:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260407000359:0",
        "title": "Big Tech and Banks Expected to Lead Solid Earnings Season. There Will Be Buying Opportunities. — Barrons.com",
        "published": 1775541600,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AVGO",
            "logoid": "broadcom"
          },
          {
            "symbol": "NYSE:JPM",
            "logoid": "jpmorgan-chase"
          },
          {
            "symbol": "NYSE:MS",
            "logoid": "morgan-stanley"
          }
        ],
        "storyPath": "/news/DJN_DN20260407000359:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L4N40Q06P:0",
        "title": "Apple's foldable iPhone faces engineering snags, potential shipment delays, Nikkei Asia reports",
        "published": 1775532148,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L4N40Q06P:0-apple-s-foldable-iphone-faces-engineering-snags-potential-shipment-delays-nikkei-asia-reports/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L4N40Q061:0",
        "title": "Apple's foldable iPhone encounters engineering snags, faces potential shipment delays, Nikkei Asia reports",
        "published": 1775530403,
        "urgency": 1,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L4N40Q061:0-apple-s-foldable-iphone-encounters-engineering-snags-faces-potential-shipment-delays-nikkei-asia-reports/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260406003372:0",
        "title": "AI Is Squeezing Memory Supplies. How Apple's Strategy Can Boost Its Stock. — Barrons.com",
        "published": 1775492760,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:DELL",
            "logoid": "dell"
          },
          {
            "symbol": "NYSE:HPQ",
            "logoid": "hp"
          }
        ],
        "storyPath": "/news/DJN_DN20260406003372:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_SN20260406003478:0",
        "title": "Apple's stock could surge 20%, and the MacBook Neo could be a key catalyst",
        "published": 1775492640,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_SN20260406003478:0/",
        "provider": {
          "id": "market-watch",
          "name": "MarketWatch",
          "logo_id": "marketwatch"
        }
      },
      {
        "id": "DJN_DN20260403001003:0",
        "title": "SpaceX Is Worth $2 Trillion? What That Might Mean. — Barrons.com",
        "published": 1775244360,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          }
        ],
        "storyPath": "/news/DJN_DN20260403001003:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260403002001:0",
        "title": "I Looked Inside the First iPhone and Saw 50 Years of Apple History — WSJ",
        "published": 1775231100,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260403002001:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_SN20260402006665:0",
        "title": "Venture capitalist who bet on Apple nearly 50 years ago: Questionable management, price is rich, but 'home-hobby computers' are hot",
        "published": 1775140260,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_SN20260402006665:0/",
        "provider": {
          "id": "market-watch",
          "name": "MarketWatch",
          "logo_id": "marketwatch"
        }
      },
      {
        "id": "dpa_afx:4ad72a40de37f:0",
        "title": "Apple @ 50: Five Decades Of Reinvention",
        "published": 1775052285,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/dpa_afx:4ad72a40de37f:0-apple-50-five-decades-of-reinvention/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "DJN_DN20260401002674:0",
        "title": "Buffett Isn't Getting Carried Away by This Iran Trump Bump. Neither Should Markets. — Barrons.com",
        "published": 1775039580,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:CEG",
            "logoid": "constellation-energy-cad-hedged-cibc-cdr"
          },
          {
            "symbol": "NYSE:DIS",
            "logoid": "walt-disney"
          },
          {
            "symbol": "NYSE:LMT",
            "logoid": "lockheed-martin"
          },
          {
            "symbol": "NYSE:NOC",
            "logoid": "northrop-grumman"
          }
        ],
        "storyPath": "/news/DJN_DN20260401002674:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L4N40K0QN:0",
        "title": "Apple's 50-year journey from garage to tech titan",
        "published": 1775037600,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L4N40K0QN:0-apple-s-50-year-journey-from-garage-to-tech-titan/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260331006152:0",
        "title": "Apple Turns 50. The iPhone Can't Drive the Stock Forever. — Barrons.com",
        "published": 1774988580,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260331006152:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260331008339:0",
        "title": "Apple Expected to Detail AI Advancements at 2026 WWDC — Market Talk",
        "published": 1774977600,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260331008339:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L4N40J1QM:0",
        "title": "Apple tests Siri feature that handles multiple commands at once, Bloomberg News reports",
        "published": 1774974295,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L4N40J1QM:0-apple-tests-siri-feature-that-handles-multiple-commands-at-once-bloomberg-news-reports/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260331004886:0",
        "title": "Warren Buffett Sees Little to Buy in the Stock Market After This Year's Drop — Barrons.com",
        "published": 1774971360,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NYSE:BRK.A",
            "logoid": "berkshire-hathaway"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "TVC:DJI",
            "logoid": "indices/dow-30"
          }
        ],
        "storyPath": "/news/DJN_DN20260331004886:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260331006959:0",
        "title": "Apple Price Target Maintained With a $350.00/Share by Wedbush",
        "published": 1774968840,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260331006959:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L6N40J177:0",
        "title": "Warren Buffett discusses markets, Apple, Jeffrey Epstein, Gates Foundation on CNBC",
        "published": 1774962093,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NYSE:BRK.A",
            "logoid": "berkshire-hathaway"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L6N40J177:0-warren-buffett-discusses-markets-apple-jeffrey-epstein-gates-foundation-on-cnbc/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260329000049:0",
        "title": "Correction to Everyone Hates iPhone Autocorrect Article on March 29 — WSJ",
        "published": 1774897860,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260329000049:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "dpa_afx:46d65658f83f8:0",
        "title": "UK Fines Apple Subsidiary £390,000 Over Russia Sanctions Breach",
        "published": 1774882533,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/dpa_afx:46d65658f83f8:0-uk-fines-apple-subsidiary-390-000-over-russia-sanctions-breach/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L8N40F0VG:0",
        "title": "What is the World Trade Organization e-commerce moratorium?",
        "published": 1774704337,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L8N40F0VG:0-what-is-the-world-trade-organization-e-commerce-moratorium/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L6N40F11D:0",
        "title": "Apple hires ex-Google executive to head AI marketing amid push to improve Siri",
        "published": 1774632658,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L6N40F11D:0-apple-hires-ex-google-executive-to-head-ai-marketing-amid-push-to-improve-siri/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260327005265:0",
        "title": "All Eyes Back on Apple's AI Strategy As 50th Anniversary — Market Talk",
        "published": 1774617540,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260327005265:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260326010953:0",
        "title": "Netflix's Prices Are Going Up. Don't Expect Streaming to Get Cheaper Soon. — Barrons.com",
        "published": 1774614540,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:DIS",
            "logoid": "walt-disney"
          },
          {
            "symbol": "NASDAQ:NFLX",
            "logoid": "netflix"
          },
          {
            "symbol": "NASDAQ:PSKY",
            "logoid": "viacomcbs"
          }
        ],
        "storyPath": "/news/DJN_DN20260326010953:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "dpa_afx:8a7391661267a:0",
        "title": "Apple Adds New Partners, To Invest $400 Mln To Expand US Manufacturing",
        "published": 1774611960,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "TSE:6762",
            "logoid": "tdk"
          },
          {
            "symbol": "NASDAQ:CRUS",
            "logoid": "cirrus-logic"
          }
        ],
        "storyPath": "/news/dpa_afx:8a7391661267a:0-apple-adds-new-partners-to-invest-400-mln-to-expand-us-manufacturing/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN40E16L:0",
        "title": "Apple Has Discontinued Mac Pro And Has Removed It From Its Website - Bloomberg News Reporter Gurman",
        "published": 1774559227,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN40E16L:0-apple-has-discontinued-mac-pro-and-has-removed-it-from-its-website-bloomberg-news-reporter-gurman/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN40E16J:0",
        "title": "Apple Gives iPhone Designers Rare Bonuses To Fight OpenAI Poaching - Bloomberg News",
        "published": 1774557668,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN40E16J:0-apple-gives-iphone-designers-rare-bonuses-to-fight-openai-poaching-bloomberg-news/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260326009594:0",
        "title": "Apple Stock Has Been Weak This Year. Why Analysts Think Better Times Are Ahead. — Barrons.com",
        "published": 1774557000,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260326009594:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN40E14R:0",
        "title": "Apple Plans To Open Up Siri To Rival AI Assistants In iOS 27 Update - Bloomberg News",
        "published": 1774548846,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN40E14R:0-apple-plans-to-open-up-siri-to-rival-ai-assistants-in-ios-27-update-bloomberg-news/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L4N40E0ZU:0",
        "title": "Apple adds Bosch, Cirrus Logic, others to US manufacturing program, to invest $400 million",
        "published": 1774530538,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:CRUS",
            "logoid": "cirrus-logic"
          },
          {
            "symbol": "TSE:6762",
            "logoid": "tdk"
          },
          {
            "symbol": "NYSE:Q",
            "logoid": "qnity-electronics"
          },
          {
            "symbol": "TWSE:2330",
            "logoid": "taiwan-semiconductor"
          },
          {
            "symbol": "NASDAQ:GFS",
            "logoid": "globalfoundries"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L4N40E0ZU:0-apple-adds-bosch-cirrus-logic-others-to-us-manufacturing-program-to-invest-400-million/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260325006992:0",
        "title": "Microsoft Stock Tracking Worst 6-Month Stretch Since 2009 — Barrons.com",
        "published": 1774471980,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AVGO",
            "logoid": "broadcom"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NYSE:SNOW",
            "logoid": "snowflake"
          }
        ],
        "storyPath": "/news/DJN_DN20260325006992:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260325007265:0",
        "title": "Amplification for Apple Cuts App Store Fees in China Article on March 13 — WSJ",
        "published": 1774464720,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260325007265:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "dpa_afx:b59c1ac2b1b02:0",
        "title": "Apple Introduces Age Verification For UK Users",
        "published": 1774455929,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/dpa_afx:b59c1ac2b1b02:0-apple-introduces-age-verification-for-uk-users/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_P8N3ZR082:0",
        "title": "February shipments of foreign-branded phones in China fall 7.7% from a year ago, CAICT data shows",
        "published": 1774420658,
        "urgency": 1,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_P8N3ZR082:0-february-shipments-of-foreign-branded-phones-in-china-fall-7-7-from-a-year-ago-caict-data-shows/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260324008889:0",
        "title": "HP Inc. Announces AI Updates. Your Turn, Apple. — Barrons.com",
        "published": 1774388400,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:HPQ",
            "logoid": "hp"
          }
        ],
        "storyPath": "/news/DJN_DN20260324008889:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN40C10O:0",
        "title": "Apple Plans AI Reboot With Siri App, New Look And ‘Ask Siri’ Button In IOS 27 - Bloomberg News",
        "published": 1774378664,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN40C10O:0-apple-plans-ai-reboot-with-siri-app-new-look-and-ask-siri-button-in-ios-27-bloomberg-news/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L1N40C0TO:0",
        "title": "Apple to bring paid ads to maps to US, Canada this summer",
        "published": 1774367569,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L1N40C0TO:0-apple-to-bring-paid-ads-to-maps-to-us-canada-this-summer/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L6N40C0UP:0",
        "title": "Apple to bring paid ads to maps to US, Canada this summer ",
        "published": 1774364400,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L6N40C0UP:0-apple-to-bring-paid-ads-to-maps-to-us-canada-this-summer/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260323006307:0",
        "title": "Apple iPhone Demand Is Getting Multiple Boosts, Analysts Say. The Stock Rises. — Barrons.com",
        "published": 1774289700,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260323006307:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260323006259:0",
        "title": "Apple Price Target Maintained With a $315.00/Share by Morgan Stanley",
        "published": 1774289100,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260323006259:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L4N40B1LQ:0",
        "title": "Apple to hold annual developers conference from June 8",
        "published": 1774287883,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L4N40B1LQ:0-apple-to-hold-annual-developers-conference-from-june-8/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L4N40B1L0:0",
        "title": "Apple to hold annual developers conference in June",
        "published": 1774285485,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L4N40B1L0:0-apple-to-hold-annual-developers-conference-in-june/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN40B0TN:0",
        "title": "Apple Is Set To Add Search Advertising To Maps In Services Push, An Announcement Could Come As Early As This Month- Bloomberg News",
        "published": 1774284697,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN40B0TN:0-apple-is-set-to-add-search-advertising-to-maps-in-services-push-an-announcement-could-come-as-early-as-this-month-bloomberg-news/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L6N40815C:0",
        "title": "Amazon plans smartphone comeback more than a decade after Fire Phone flop",
        "published": 1774041610,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "isExclusive": true,
        "storyPath": "/news/reuters.com,2026:newsml_L6N40815C:0-amazon-plans-smartphone-comeback-more-than-a-decade-after-fire-phone-flop/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260320006638:0",
        "title": "Apple's Latest Launch Was 'Best' Ever for New Mac Customers. What It Means for the Stock. — Barrons.com",
        "published": 1774038720,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:DELL",
            "logoid": "dell"
          },
          {
            "symbol": "NYSE:HPQ",
            "logoid": "hp"
          }
        ],
        "storyPath": "/news/DJN_DN20260320006638:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_P8N3YM04J:0",
        "title": "China's commerce minister meets Apple CEO",
        "published": 1773995981,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_P8N3YM04J:0-china-s-commerce-minister-meets-apple-ceo/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260319007716:0",
        "title": "Apple's China iPhone Sales Are Up. Thank Memory Cost Increases. — Barrons.com",
        "published": 1773942660,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260319007716:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L6N3WF0SO:0",
        "title": "Apple fends off bid for new Apple Watch import ban at US trade tribunal ",
        "published": 1773936720,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MASI",
            "logoid": "masimo"
          },
          {
            "symbol": "NYSE:DHR",
            "logoid": "danaher"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L6N3WF0SO:0-apple-fends-off-bid-for-new-apple-watch-import-ban-at-us-trade-tribunal/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L8N40701A:0",
        "title": "Apple's China smartphone sales jump 23% to start 2026, bucking industry trend",
        "published": 1773886610,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L8N40701A:0-apple-s-china-smartphone-sales-jump-23-to-start-2026-bucking-industry-trend/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260318009535:0",
        "title": "Apple Is Way Behind in AI — and Still Making a Fortune From It — WSJ",
        "published": 1773882000,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260318009535:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260318001539:0",
        "title": "Sure, Nvidia Stock Is Stuck. But Don't Ignore Its Huge Cash Returns. — Barrons.com",
        "published": 1773864480,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/DJN_DN20260318001539:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN4060M6:0",
        "title": "Apple Says Some AI Vibe Coding Apps Violate App Store Rules By Running Code That Alters App Functionality - The Information",
        "published": 1773839002,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN4060M6:0-apple-says-some-ai-vibe-coding-apps-violate-app-store-rules-by-running-code-that-alters-app-functionality-the-information/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260318000052:0",
        "title": "Apple's App Store Fee Cut in China Offers Tailwind for Tencent, NetEase — Market Talk",
        "published": 1773807120,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NTES",
            "logoid": "netease"
          },
          {
            "symbol": "HKEX:700",
            "logoid": "tencent"
          }
        ],
        "storyPath": "/news/DJN_DN20260318000052:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:adc733d48094b:0",
        "title": "Apple Loses Top Hardware Executive To Smart Ring Maker Oura Health Amid Product Delays: Report",
        "published": 1773786003,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-loses-top-hardware-executive-to-smart-ring-maker-oura-health-amid-product-delays-report/cZ3Ek3bRIXx",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:adc733d48094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN4050SG:0",
        "title": "Apple’S Head Of Home Hardware Brian Lynch Leaves For Smart Ring Maker Oura - Bloomberg News",
        "published": 1773785305,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN4050SG:0-apple-s-head-of-home-hardware-brian-lynch-leaves-for-smart-ring-maker-oura-bloomberg-news/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260317006382:0",
        "title": "Apple CEO Squashes Talk of Stepping Down — Market Talk",
        "published": 1773767340,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260317006382:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:ec5a08cb6094b:0",
        "title": "Apple’s Tim Cook Shuts Down Retirement Buzz, Says He ‘Deeply’ Loves His Job",
        "published": 1773765924,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-tim-cook-shuts-down-retirement-buzz-says-he-deeply-loves-his-job/cZ3Ea4yRIXk",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:ec5a08cb6094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "dpa_afx:5b58a8bad361e:0",
        "title": "Apple Launches AirPods Max 2 With Improved ANC And H2 Chip",
        "published": 1773685935,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/dpa_afx:5b58a8bad361e:0-apple-launches-airpods-max-2-with-improved-anc-and-h2-chip/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "DJN_DN20260316006424:0",
        "title": "Apple Acquires MotionVFX",
        "published": 1773680700,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260316006424:0-apple-acquires-motionvfx/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260316005558:0",
        "title": "Apple Announced AirPods Max 2, Starting at $549 — Market Talk",
        "published": 1773676260,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260316005558:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L6N4040XN:0",
        "title": "Apple unveils second-generation AirPods Max at $549, more than five years after debut",
        "published": 1773668798,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "TSE:6758",
            "logoid": "sony"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L6N4040XN:0-apple-unveils-second-generation-airpods-max-at-549-more-than-five-years-after-debut/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260314000775:0",
        "title": "Review: Does the $599 MacBook Neo Fit in Your Life? — WSJ",
        "published": 1773495120,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260314000775:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260313003272:0",
        "title": "Apple Reduces China App Store Fees as It Fends Off Pressure From Beijing — Barrons.com",
        "published": 1773409860,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260313003272:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260313004404:0",
        "title": "Meta Is Falling Behind in AI Models. Its Loss Could Be Google's Gain, Report Says. — Barrons.com",
        "published": 1773408240,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          }
        ],
        "storyPath": "/news/DJN_DN20260313004404:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:0fcb83f3b094b:0",
        "title": "Apple Bows To Chinese Regulatory Pressure With App Store Fee Cut: These Firms Could Be The Big Winners",
        "published": 1773391474,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-bows-to-chinese-regulatory-pressure-with-app-store-fee-cut/cZdDEsRRIaN",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:0fcb83f3b094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_DN20260313001151:0",
        "title": "Apple Cuts App Store Fees in China as Regulatory Scrutiny Intensifies — Update",
        "published": 1773384300,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260313001151:0-apple-cuts-app-store-fees-in-china-as-regulatory-scrutiny-intensifies-update/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260313000127:0",
        "title": "Apple's Commission Cut Bodes Well for Chinese Game Developers — Market Talk",
        "published": 1773378360,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:NTES",
            "logoid": "netease"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "HKEX:700",
            "logoid": "tencent"
          }
        ],
        "storyPath": "/news/DJN_DN20260313000127:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260312013664:0",
        "title": "Apple Cuts App Store Commission Fees in China",
        "published": 1773374160,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260312013664:0-apple-cuts-app-store-commission-fees-in-china/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:7499a5168094b:0",
        "title": "Is Himax A ‘Stealth’ Supplier To Nvidia, Apple? HIMX Stock Pops To Nearly 1-Year High After Hedge Fund Flags Possible Links",
        "published": 1773368534,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/is-himax-a-stealth-supplier-to-nvidia-apple-himx-stock-pops-to-nearly-1-year-high-after-hedge-fund-flags-possible-links/cZdwxZ1RIaB",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:HIMX",
            "logoid": "himax-technologies"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/stocktwits:7499a5168094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_DN20260312013523:0",
        "title": "Global Smartphone Shipments Could Fall 17% in 2026 — Market Talk",
        "published": 1773368280,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "KRX:005930",
            "logoid": "samsung"
          },
          {
            "symbol": "HKEX:1810",
            "logoid": "xiaomi"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260312013523:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260312012252:0",
        "title": "Monster, Palantir, and Other Stocks That Can Weather the Market Storm — Barrons.com",
        "published": 1773352140,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MNST",
            "logoid": "monster-beverage"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:PLTR",
            "logoid": "palantir"
          }
        ],
        "storyPath": "/news/DJN_DN20260312012252:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260312007814:0",
        "title": "FTC Release: Federal Trade Commission Chairman Andrew N. Ferguson Issues Warning Letter to Apple CEO Tim Cook",
        "published": 1773329820,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260312007814:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L1N4000GL:0",
        "title": "India plans fresh incentives for phone production in boost for Apple, Samsung",
        "published": 1773315519,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "KRX:005930",
            "logoid": "samsung"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L1N4000GL:0-india-plans-fresh-incentives-for-phone-production-in-boost-for-apple-samsung/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN3ZZ16X:0",
        "title": "Apple's Forthcoming Foldable iPhone Will Feature An Interior Foldable Display Roughly The Size Of An iPad Mini - Bloomberg News",
        "published": 1773260038,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN3ZZ16X:0-apple-s-forthcoming-foldable-iphone-will-feature-an-interior-foldable-display-roughly-the-size-of-an-ipad-mini-bloomberg-news/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "stocktwits:6fb9f49d5094b:0",
        "title": "Laptop Prices Could Rise Up To 40% In 2026: How Apple, HP And Dell Are Plotting To Navigate Rising Memory Prices",
        "published": 1773220767,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/laptop-prices-could-rise-up-to-40-in-2026-how-apple-hp-and-dell-are-plotting-to-navigate-rising-memory-prices/cZdAMLuRIJf",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NYSE:DELL",
            "logoid": "dell"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:HPQ",
            "logoid": "hp"
          }
        ],
        "storyPath": "/news/stocktwits:6fb9f49d5094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_DN20260310008536:0",
        "title": "Apple's Budget MacBook Is a Hit. What It Means For the Stock, and What's Next. — Barrons.com",
        "published": 1773167940,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260310008536:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260310005451:0",
        "title": "German Ad Groups Say Changes to Apple's App-Tracking Tool Aren't Enough",
        "published": 1773146400,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260310005451:0-german-ad-groups-say-changes-to-apple-s-app-tracking-tool-aren-t-enough/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:fca095bd1094b:0",
        "title": "Apple Delays Smart Home Device Once More Amid New AI, Siri Setback: Report",
        "published": 1773082815,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-delays-smart-home-device-once-more-amid-new-ai-siri-setback-report/cZdVuFuRIeR",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:fca095bd1094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN3ZX125:0",
        "title": "Apple Postpones Smart Home Display Launch As It Waits For New AI, Siri - Bloomberg News",
        "published": 1773082443,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN3ZX125:0-apple-postpones-smart-home-display-launch-as-it-waits-for-new-ai-siri-bloomberg-news/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260309003955:0",
        "title": "Apple Faces a Memory Crunch. Why Analysts Say the Stock Is Still a Buy. — Barrons.com",
        "published": 1773057780,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260309003955:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260305001184:0",
        "title": "Up & Down Wall Street: How the Mag 7 Became the Lag 7 — Barron's",
        "published": 1772850600,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          }
        ],
        "storyPath": "/news/DJN_DN20260305001184:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260306006471:0",
        "title": "3 Dividend ETFs for Shelter in These Stormy Times — Barrons.com",
        "published": 1772820900,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AVGO",
            "logoid": "broadcom"
          },
          {
            "symbol": "NYSE:KO",
            "logoid": "coca-cola"
          },
          {
            "symbol": "NYSE:COP",
            "logoid": "conocophillips"
          },
          {
            "symbol": "NYSE:LMT",
            "logoid": "lockheed-martin"
          }
        ],
        "storyPath": "/news/DJN_DN20260306006471:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:bad99ff54094b:0",
        "title": "‘Big Short’ Fame Michael Burry Pitches Bold AI Deal Ideas For Apple, Adobe — And Fires Shots At Tesla CEO Elon Musk",
        "published": 1772772649,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/big-short-fame-michael-burry-pitches-bold-ai-deal-ideas-for-apple-adobe-and-fires-shots-at-tesla-ceo-elon-musk/cZdhnSmRIEJ",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:ANTHROPIC",
            "logoid": "anthropic"
          }
        ],
        "storyPath": "/news/stocktwits:bad99ff54094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_DN20260305009360:0",
        "title": "This ETF Was Built for This Very Moment. So Why Hasn't It Done Well? — Barrons.com",
        "published": 1772746980,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/DJN_DN20260305009360:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260305009544:0",
        "title": "Cheaper iPhones and a $599 MacBook? Apple Is All About Affordability Now. — Barrons.com",
        "published": 1772746680,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:DELL",
            "logoid": "dell"
          },
          {
            "symbol": "NYSE:HPQ",
            "logoid": "hp"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/DJN_DN20260305009544:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "dpa_afx:7cb6395cea3f4:0",
        "title": "Apple Music To Add Transparency Tags For AI-Generated Music",
        "published": 1772744961,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/dpa_afx:7cb6395cea3f4:0-apple-music-to-add-transparency-tags-for-ai-generated-music/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "DJN_DN20260305006608:0",
        "title": "Apple Is Maintained at Neutral by Rosenblatt",
        "published": 1772718960,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260305006608:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260304012892:0",
        "title": "MacBook Neo and iPhone 17e First Impressions: The Return of Cheap and Cheerful — Personal Technology — WSJ",
        "published": 1772676000,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260304012892:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "dpa_afx:2859ab73a8cb7:0",
        "title": "Apple Launches MacBook Neo Starting At $599",
        "published": 1772649459,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/dpa_afx:2859ab73a8cb7:0-apple-launches-macbook-neo-starting-at-599/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "DJN_DN20260304007584:0",
        "title": "Apple's Price Increases Soothe Concerns Over Memory Costs — Market Talk",
        "published": 1772645640,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260304007584:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260304006806:0",
        "title": "Apple Launches a $599 MacBook. Why That Price Is Such a Big Deal. — Barrons.com",
        "published": 1772644500,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:DELL",
            "logoid": "dell"
          },
          {
            "symbol": "NYSE:HPQ",
            "logoid": "hp"
          }
        ],
        "storyPath": "/news/DJN_DN20260304006806:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260304007387:0",
        "title": "Apple Uses Low Prices to Attack Rivals During Memory-Chip Crunch — WSJ",
        "published": 1772644260,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260304007387:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260304007302:0",
        "title": "Apple Seen Getting a Lift from New Mac Laptops — Market Talk",
        "published": 1772644080,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260304007302:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:930831ece094b:0",
        "title": "Apple Launches MacBook Neo At $599, Offering An Alternative To Google’s Chromebooks",
        "published": 1772639380,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-launches-macbook-neo-starting-at-599-taking-on-google-chromebooks/cZd9YtyRI5z",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:930831ece094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_DN20260304006275:0",
        "title": "Apple's $599 MacBook Neo: The Pros and Cons — WSJ",
        "published": 1772637960,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260304006275:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L6N3ZS157:0",
        "title": "Apple debuts $599 MacBook Neo to challenge Chromebooks, Windows PCs",
        "published": 1772634439,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:ARM",
            "logoid": "arm"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L6N3ZS157:0-apple-debuts-599-macbook-neo-to-challenge-chromebooks-windows-pcs/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "stocktwits:ec0a965c0094b:0",
        "title": "AAPL, MSFT, CRWD, PANW: Dan Ives Identifies Top Tech Names Positioned To Navigate US-Iran War-Led Volatility",
        "published": 1772632599,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/aapl-msft-crwd-panw-dan-ives-identifies-top-tech-names-positioned-to-navigate-us-iran-war-led-volatility/cZd9VsnRI5t",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:CRWD",
            "logoid": "crowdstrike"
          },
          {
            "symbol": "NASDAQ:PANW",
            "logoid": "palo-alto-networks"
          }
        ],
        "storyPath": "/news/stocktwits:ec0a965c0094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_P8N3YS0DA:0",
        "title": "Shipments of foreign-branded phones in China fell in Jan on-year, CAICT data says",
        "published": 1772589432,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_P8N3YS0DA:0-shipments-of-foreign-branded-phones-in-china-fell-in-jan-on-year-caict-data-says/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "dpa_afx:17468bd159475:0",
        "title": "Apple Explores Deepening Google Partnership For Next-Gen Siri",
        "published": 1772576758,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/dpa_afx:17468bd159475:0-apple-explores-deepening-google-partnership-for-next-gen-siri/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "dpa_afx:916e3ad594757:0",
        "title": "Apple Unveils New Studio Display Lineup, Introduces Studio Display XDR",
        "published": 1772574784,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/dpa_afx:916e3ad594757:0-apple-unveils-new-studio-display-lineup-introduces-studio-display-xdr/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "DJN_DN20260303008032:0",
        "title": "This Schwab Dividend ETF is a Superstar. Defense and Energy Are Key — Barrons.com",
        "published": 1772566800,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AVGO",
            "logoid": "broadcom"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:MORN",
            "logoid": "morningstar"
          }
        ],
        "storyPath": "/news/DJN_DN20260303008032:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "dpa_afx:fb10a1085b6ba:0",
        "title": "Apple Launches M5 Pro And M5 Max With Major Performance Boost",
        "published": 1772563012,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/dpa_afx:fb10a1085b6ba:0-apple-launches-m5-pro-and-m5-max-with-major-performance-boost/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "dpa_afx:2c972b4358f9c:0",
        "title": "Apple Unveils MacBook Air With M5 Chip",
        "published": 1772560785,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/dpa_afx:2c972b4358f9c:0-apple-unveils-macbook-air-with-m5-chip/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "DJN_DN20260303001337:0",
        "title": "Should You Buy the Stock Market's Dip? Why the Mideast Fighting Could Be an Opportunity. — Barrons.com",
        "published": 1772556300,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/DJN_DN20260303001337:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260303006394:0",
        "title": "Apple Launches New Laptops and Chips. AI Power Is a Focus. — Barrons.com",
        "published": 1772554920,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260303006394:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260303006023:0",
        "title": "Apple Is Maintained at Underweight by Barclays",
        "published": 1772551920,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260303006023:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:bfad4995e094b:0",
        "title": "Apple Increases Prices Of Its New MacBook Air And Pro Models – Everything To Know About Its Latest Lineup",
        "published": 1772549519,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-increases-prices-of-its-new-mac-book-air-and-pro-models-everything-to-know-about-its-latest-lineup/cZdeK53RIPf",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:bfad4995e094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "dpa_afx:7f5b6e0b4c913:0",
        "title": "Apple Introduces M4-Powered IPad Air With 12GB Memory, Starting At $599",
        "published": 1772488648,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/dpa_afx:7f5b6e0b4c913:0-apple-introduces-m4-powered-ipad-air-with-12gb-memory-starting-at-599/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "stocktwits:d413ae839094b:0",
        "title": "Apple’s New iPhone 17e To Boost Sales From Price-Focused Buyers, Says Gene Munster",
        "published": 1772476910,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-iphone-17e-to-boost-sales-from-price-focused-buyers-says-gene-munster/cZd3i5GRI2W",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:d413ae839094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_DN20260302008113:0",
        "title": "Apple Faces Risk of Slower Demand for Next iPhone — Market Talk",
        "published": 1772476560,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260302008113:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "dpa_afx:843ffe90d6293:0",
        "title": "Apple Unveils IPhone 17e With A19 Chip, Improved Camera And Satellite Features",
        "published": 1772475902,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/dpa_afx:843ffe90d6293:0-apple-unveils-iphone-17e-with-a19-chip-improved-camera-and-satellite-features/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "DJN_DN20260302006227:0",
        "title": "Apple's 'Affordable' New iPhone 17e: Why You Should — or Shouldn't — Get It — WSJ",
        "published": 1772463720,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260302006227:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:7c6065ec9094b:0",
        "title": "Apple Launches iPhone 17e With A19 Chip, Advanced Camera",
        "published": 1772461866,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-launches-i-phone-17e-with-a19-chip-advanced-camera/cZd3BiGRI25",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:7c6065ec9094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN3ZQ0WW:0",
        "title": "Apple Discusses Google Hosting New Siri, Deepening Cloud Reliance- The Information",
        "published": 1772460305,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:GOOG",
            "logoid": "alphabet"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN3ZQ0WW:0-apple-discusses-google-hosting-new-siri-deepening-cloud-reliance-the-information/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260228000971:0",
        "title": "Berkshire Hathaway's CEO Suggests These 4 Companies Are Forever Stocks — Barrons.com",
        "published": 1772314920,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NYSE:AXP",
            "logoid": "american-express"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:BRK.A",
            "logoid": "berkshire-hathaway"
          },
          {
            "symbol": "NYSE:KO",
            "logoid": "coca-cola"
          },
          {
            "symbol": "NYSE:MCO",
            "logoid": "moodys"
          }
        ],
        "storyPath": "/news/DJN_DN20260228000971:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L6N3ZO0AO:0",
        "title": "Berkshire CEO Abel assures investors he'll be a careful steward after Buffett",
        "published": 1772286285,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NYSE:BRK.A",
            "logoid": "berkshire-hathaway"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:AXP",
            "logoid": "american-express"
          },
          {
            "symbol": "NYSE:KO",
            "logoid": "coca-cola"
          },
          {
            "symbol": "NYSE:MCO",
            "logoid": "moodys"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L6N3ZO0AO:0-berkshire-ceo-abel-assures-investors-he-ll-be-a-careful-steward-after-buffett/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN3ZO0B9:0",
        "title": "Berkshire Hathaway Reported $373.3 Billion Of Cash And Equivalents As Of December 31, 2025",
        "published": 1772286043,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:AXP",
            "logoid": "american-express"
          },
          {
            "symbol": "NYSE:BAC",
            "logoid": "bank-of-america"
          },
          {
            "symbol": "NYSE:BRK.A",
            "logoid": "berkshire-hathaway"
          },
          {
            "symbol": "NYSE:CVX",
            "logoid": "chevron"
          },
          {
            "symbol": "NYSE:KO",
            "logoid": "coca-cola"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN3ZO0B9:0-berkshire-hathaway-reported-373-3-billion-of-cash-and-equivalents-as-of-december-31-2025/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L6N3ZO0AF:0",
        "title": "Berkshire Hathaway profit falls on writedowns, lower insurance income",
        "published": 1772285132,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NYSE:BRK.A",
            "logoid": "berkshire-hathaway"
          },
          {
            "symbol": "NASDAQ:KHC",
            "logoid": "kraft-heinz"
          },
          {
            "symbol": "NYSE:OXY",
            "logoid": "occidental-petroleum"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:AXP",
            "logoid": "american-express"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L6N3ZO0AF:0-berkshire-hathaway-profit-falls-on-writedowns-lower-insurance-income/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "dpa_afx:a1be740354182:0",
        "title": "Apple's Latest IPhones And IPads Approved For NATO-Restricted Information",
        "published": 1772226888,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/dpa_afx:a1be740354182:0-apple-s-latest-iphones-and-ipads-approved-for-nato-restricted-information/",
        "provider": {
          "id": "dpa_afx",
          "name": "dpa-AFX",
          "logo_id": "dpa_afx"
        }
      },
      {
        "id": "DJN_DN20260227008205:0",
        "title": "How to Fight AI? The 'Rolex Effect' Could Lift Apple and Other Consumer Brands — Barrons.com",
        "published": 1772213100,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NYSE:MCD",
            "logoid": "mcdonalds"
          },
          {
            "symbol": "NASDAQ:WMT",
            "logoid": "walmart"
          }
        ],
        "storyPath": "/news/DJN_DN20260227008205:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260227005259:0",
        "title": "Stocks Are Set for a February Slide. Can the Magnificent 7 Spark a March Rebound? — Barrons.com",
        "published": 1772196000,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:TSLA",
            "logoid": "tesla"
          }
        ],
        "storyPath": "/news/DJN_DN20260227005259:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "stocktwits:a55a75590094b:0",
        "title": "Apple’s AI Woes Meet A ‘Tsunami-Like’ Shock: IDC Sees Smartphone Shipments Crashing This Year",
        "published": 1772178224,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-s-ai-woes-meet-a-tsunami-like-shock-idc-sees-smartphone-shipments-crashing-this-year/cZTc9VjRIRH",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:a55a75590094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L4N3ZM253:0",
        "title": "Smartphone market set for biggest-ever decline in 2026 on memory price surge, IDC says",
        "published": 1772133573,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "KRX:005930",
            "logoid": "samsung"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L4N3ZM253:0-smartphone-market-set-for-biggest-ever-decline-in-2026-on-memory-price-surge-idc-says/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_SN20260226013776:0",
        "title": "These S&P 500 alternatives have shined so far this year",
        "published": 1772122560,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "CBOE:SPX",
            "logoid": "indices/s-and-p-500"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "AMEX:RSP",
            "logoid": "invesco"
          },
          {
            "symbol": "NASDAQ:MSFT",
            "logoid": "microsoft"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          }
        ],
        "storyPath": "/news/DJN_SN20260226013776:0/",
        "provider": {
          "id": "market-watch",
          "name": "MarketWatch",
          "logo_id": "marketwatch"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L6N3ZM0WB:0",
        "title": "Apple seeks dismissal of fraud lawsuit over Siri AI, Epic injunction",
        "published": 1772121551,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L6N3ZM0WB:0-apple-seeks-dismissal-of-fraud-lawsuit-over-siri-ai-epic-injunction/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L4N3ZM0I5:0",
        "title": "Apple in talks with banks to start payment service in India, Bloomberg News reports",
        "published": 1772087567,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NSE:ICICIBANK",
            "logoid": "icici-bank"
          },
          {
            "symbol": "NSE:HDFCBANK",
            "logoid": "hdfc-bank"
          },
          {
            "symbol": "NSE:AXISBANK",
            "logoid": "axis-bank"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L4N3ZM0I5:0-apple-in-talks-with-banks-to-start-payment-service-in-india-bloomberg-news-reports/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN3ZL29P:0",
        "title": "Apple In Talks With Banks To Start Payment Service In India - Bloomberg News",
        "published": 1772087389,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN3ZL29P:0-apple-in-talks-with-banks-to-start-payment-service-in-india-bloomberg-news/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260225008335:0",
        "title": "What I Saw Inside Apple's U.S. Chip Supply Chain — WSJ",
        "published": 1772049240,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "TWSE:2330",
            "logoid": "taiwan-semiconductor"
          }
        ],
        "storyPath": "/news/DJN_DN20260225008335:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "DJN_DN20260225009010:0",
        "title": "Apple Needs to Copy Samsung's New Security Smartphone Screen ASAP — WSJ",
        "published": 1772043120,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "KRX:005930",
            "logoid": "samsung"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260225009010:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L1N3ZL0OL:0",
        "title": "Apple and Amazon took too long to remove anti-competitive clauses, Spanish watchdog says",
        "published": 1772030407,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L1N3ZL0OL:0-apple-and-amazon-took-too-long-to-remove-anti-competitive-clauses-spanish-watchdog-says/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260225006487:0",
        "title": "Spain Ramps Up Pressure on Apple, Amazon in Yearslong Antitrust Case",
        "published": 1772027400,
        "urgency": 2,
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260225006487:0-spain-ramps-up-pressure-on-apple-amazon-in-yearslong-antitrust-case/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L8N3ZL16B:0",
        "title": "Spain's antitrust watchdog says Apple, Amazon took too long to refine anti-competitive contracts",
        "published": 1772025565,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:AMZN",
            "logoid": "amazon"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L8N3ZL16B:0-spain-s-antitrust-watchdog-says-apple-amazon-took-too-long-to-refine-anti-competitive-contracts/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "stocktwits:7e7d034ba094b:0",
        "title": "Apple CEO Tim Cook ‘Slept With One Eye Open’ After CIA Secret Brief About China Possibly Striking Taiwan: Report",
        "published": 1771998942,
        "urgency": 2,
        "link": "https://stocktwits.com/news-articles/markets/equity/apple-ceo-tim-cook-slept-with-one-eye-open-after-cia-secret-brief-about-china-possibly-striking-taiwan/cZRUMiIR469",
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/stocktwits:7e7d034ba094b:0/",
        "provider": {
          "id": "stocktwits",
          "name": "Stocktwits",
          "logo_id": "stocktwits",
          "url": "https://stocktwits.com/"
        }
      },
      {
        "id": "DJN_DN20260224014448:0",
        "title": "Review and Preview: On Claude Nine — Barrons.com",
        "published": 1771980480,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AMD",
            "logoid": "advanced-micro-devices"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:LZ",
            "logoid": "legalzoom"
          },
          {
            "symbol": "NYSE:SNOW",
            "logoid": "snowflake"
          }
        ],
        "storyPath": "/news/DJN_DN20260224014448:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_FWN3ZK1ES:0",
        "title": "Apple’s Touch-Screen Macbook Pro To Have Dynamic Island, New Interface - Bloomberg News",
        "published": 1771967467,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_FWN3ZK1ES:0-apple-s-touch-screen-macbook-pro-to-have-dynamic-island-new-interface-bloomberg-news/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      },
      {
        "id": "DJN_DN20260224008928:0",
        "title": "Apple Vowed to Boost U.S. Manufacturing. The Mac Mini Will Be Built in This City. — Barrons.com",
        "published": 1771965600,
        "urgency": 2,
        "permission": "provider",
        "relatedSymbols": [
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          }
        ],
        "storyPath": "/news/DJN_DN20260224008928:0/",
        "provider": {
          "id": "dow-jones",
          "name": "Dow Jones Newswires",
          "logo_id": "dow-jones-newswires"
        }
      },
      {
        "id": "tag:reuters.com,2026:newsml_L4N3ZK1K3:0",
        "title": "Wall St rebounds from tech rout; tariff, AI worries linger",
        "published": 1771953683,
        "urgency": 2,
        "permission": "headline",
        "relatedSymbols": [
          {
            "symbol": "NYSE:CRM",
            "logoid": "salesforce"
          },
          {
            "symbol": "DJ:DJI",
            "logoid": "indices/dow-30"
          },
          {
            "symbol": "SP:SPX",
            "logoid": "indices/s-and-p-500"
          },
          {
            "symbol": "TVC:IXIC",
            "logoid": "indices/nasdaq-composite"
          },
          {
            "symbol": "SP:SPF",
            "logoid": "sector/financial"
          },
          {
            "symbol": "NASDAQ:AAPL",
            "logoid": "apple"
          },
          {
            "symbol": "NASDAQ:NVDA",
            "logoid": "nvidia"
          },
          {
            "symbol": "NASDAQ:AMD",
            "logoid": "advanced-micro-devices"
          },
          {
            "symbol": "NASDAQ:META",
            "logoid": "meta-platforms"
          },
          {
            "symbol": "NYSE:HD",
            "logoid": "home-depot"
          },
          {
            "symbol": "NYSE:KEYS",
            "logoid": "keysight-technologies"
          },
          {
            "symbol": "TVC:DJI",
            "logoid": "indices/dow-30"
          }
        ],
        "storyPath": "/news/reuters.com,2026:newsml_L4N3ZK1K3:0-wall-st-rebounds-from-tech-rout-tariff-ai-worries-linger/",
        "provider": {
          "id": "reuters",
          "name": "Reuters",
          "logo_id": "reuters"
        }
      }
    ],
    "streaming": {
      "channel": "64e27170d46efffb047e96cec6c2"
    },
    "pagination": {
      "cursor": "eyJfaWQiOiJzdG9ja3R3aXRzOmI4ZWY4OTFmNTA5NGIiLCJwdWJkYXRlIjoxNzcxOTUxMjk3MDAwfQ=="
    }
  },
  "msg": "Success"
}
```

## Get News Details

`GET /api/news/{newsId}`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/api/news/tag%3Areuters.com%2C2025%3Anewsml_L1N3XK042%3A0?lang=en' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": {
    "shortDescription": "At least 10 people were killed and 20 were injured after a bus carrying school children fell off a cliff in rural area in northern Colombia, the local governor said on Sunday.In a post on X, the governor of Antioquia, Andres Julian, said the bus was traveling from the Caribbean town of Tolu to Mede…",
    "astDescription": {
      "type": "root",
      "children": [
        {
          "type": "p",
          "children": [
            "At least 10 people were killed and 20 were injured after a bus carrying school children fell off a cliff in rural area in northern Colombia, the local governor said on Sunday."
          ]
        },
        {
          "type": "p",
          "children": [
            "In a post on X, the governor of Antioquia, Andres Julian, said the bus was traveling from the Caribbean town of Tolu to Medellin after a school trip and was carrying students from the Antioqueño High School. "
          ]
        },
        {
          "type": "p",
          "children": [
            "\"Until now, there are more than 10 dead and 20 injured, Julian said. \"The whole hospital network is ready to attend and support this emergency.\" "
          ]
        }
      ]
    },
    "language": "en",
    "tags": [
      {
        "title": "Reuters",
        "args": [
          {
            "id": "provider",
            "value": "reuters"
          }
        ]
      }
    ],
    "copyright": "Copyright Thomson Reuters 2025. Click For Restrictions - https://agency.reuters.com/en/copyright.html",
    "id": "tag:reuters.com,2025:newsml_L1N3XK042:0",
    "title": "Over 10 dead after school bus accident in Colombia",
    "published": 1765728766,
    "urgency": 2,
    "permission": "headline",
    "storyPath": "/news/reuters.com,2025:newsml_L1N3XK042:0-over-10-dead-after-school-bus-accident-in-colombia/",
    "read_time": 22,
    "provider": {
      "id": "reuters",
      "name": "Reuters",
      "logo_id": "reuters"
    },
    "distributor": {
      "id": "refinitiv",
      "name": "Refinitiv",
      "logo_id": "refinitiv"
    }
  },
  "msg": "Success"
}
```
