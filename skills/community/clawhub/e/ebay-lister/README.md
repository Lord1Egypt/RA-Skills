# 🏷️ eBay Lister

**Snap a photo of something you want to sell and get a live eBay listing back.** One photo is
usually enough, add more if the item needs them.

It works out what the item is, checks what the same thing actually sold for, judges the
condition, fills in eBay's listing form in a Chrome you are already signed into, and publishes.

Most eBay tooling stops at a draft or just scrapes search results. This one drives the real form
all the way to a live listing. Ships as an [OpenClaw](https://openclaw.ai) skill, but `list.js`
is plain Node plus playwright-core and works standalone.

## ✨ What you get

- 📝 Title, description, category, condition, photos, price, format, duration, and shipping, filled in for you
- 💰 Pricing from **sold** comps, not from what other people are hopefully asking
- 🎯 eBay's item-specifics widgets handled: dropdowns, multi-selects, free-text fields
- 🚀 Publishes for real, or saves a draft with `--mode draft`
- 🔁 Prints `DRAFT_ID=` every run, so a failed publish resumes instead of leaving duplicates behind
- 🔒 Never sees your password: it attaches to a browser session you already own

## 📦 Install

```bash
git clone https://github.com/NelsonScott/ebay-lister
cd ebay-lister
npm install
cp ebay-lister.config.example.json ebay-lister.config.json   # optional, defaults are sane
```

Or as an OpenClaw skill:

```bash
openclaw skills install @nelsonscott/ebay-lister
```

## 🔌 Requires

A Chrome with remote debugging enabled, already signed in to eBay:

```bash
# macOS example; any Chrome/Chromium works, any free port
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=18800 \
  --user-data-dir="$HOME/.ebay-lister-chrome"
```

Sign in to eBay once in that window, then point `cdpUrl` in your config at the same port.

## 🚀 Use

```bash
node list.js --payload-file payload.json --mode publish                    # publish
node list.js --payload-file payload.json --mode draft                      # save a draft
node list.js --payload-file payload.json --draft-id 12345 --mode publish   # resume a draft
node list.js --payload-file payload.json --dry-run                         # plan only
```

The payload is a JSON object describing the listing. [`SKILL.md`](SKILL.md) documents its full
shape and the agent-facing workflow for building one from your photos.

## ⚙️ Configuration

`ebay-lister.config.json` (gitignored, copy from the example) holds your defaults:

| Key | What it does |
|---|---|
| `cdpUrl` | Where your signed-in Chrome is listening |
| `bestOffer` | `off` by default |
| `format` | Auction vs fixed price, starting bid, duration |
| `shipping.service` | Preferred shipping service |
| `categoryIds` | Keyword to category-ID shortcuts |
| `notifyCommand` | Optional command to run when a listing goes live |

## ⚠️ Known limitations

- **eBay.com (US) only.** Other eBay sites lay the form out differently and are untested.
- **Item specifics are the fragile part.** eBay renders them differently per category, and some
  categories demand aspects your payload may not supply. The script expands the section, fills
  free-text and dropdown aspects, verifies each one, and reports the ones it could not set, but a
  category with unusual widgets can still block a publish. When that happens it saves a draft
  rather than publishing something wrong.
- **Photos must be local files.** Remote URLs are not fetched for you.
- **Check the price.** Sold-comp research narrows the range, it does not replace your judgment
  on condition and completeness.
- **eBay changes its DOM.** Selectors track the current listing flow, so expect the occasional
  break after an eBay redesign.

## 📄 License

MIT
