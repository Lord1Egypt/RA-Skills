---
name: douyin-keyword-collector
description: Accessing the Douyin homepage through browser automation, entering keywords in the search bar and collecting relevant keyword suggestions in the automated prompt box.
---

# Douyin keyword collection tool

## Feature Overview

This skill automatically accesses the Douyin homepage through the browser, enters keywords in the search bar and collects relevant keyword suggestions in the automatic prompt box. No API key required, completely browser-based automation.

## Triggers

This skill is triggered when the user mentions any of the following keywords:
- 抖音关键词
- 收集抖音关键词
- 抖音搜索建议
- 抖音热门词
- 抖音 SEO
- 抖音话题
- Douyin keywords
- Collect Douyin keywords
- Douyin search suggestions
- Douyin hot words
- Douyin SEO
- Douyin topics

## Usage Scenarios

- Douyin SEO Keyword Research
- Content creation inspiration collection
- Trending topic trend analysis
- Competitive keyword research
- Short video topic selection planning

## Operation process

### 1. Launch the browser

Use the `browser` tool's `start` or `snapshot` action to launch the browser.

### 2. Visit the Douyin homepage

Navigate to the official website of Douyin:
```
https://www.douyin.com
```

### 3. Check and close the login pop-up

Use the `snapshot` action of the `browser` tool to get a page element reference and check for a login pop-up.

If there is a login pop-up (look for a close button, usually an `img` or `button` element), use the `act` action to click close:
```
browser action=act request={"kind":"click","ref"<关闭按钮引用>:""}
```

### 4. Locate the search bar

Use the `snapshot` action of the `browser` tool to get a page element reference and find the search bar input box (textbox type, description contains 'search').

### 5. Enter a keyword

Using the `act` action of the `browser` tool, select the `type` type and enter your target keyword in the search bar:
```
browser action=act request={"kind":"type","ref":"<搜索栏引用>","text":"<关键词>"}
```

### 6. Wait for the prompt box to appear

Wait 1-2 seconds for the auto prompt box to load:
```
browser action=act request={"kind":"wait","timeMs":2000}
```

### 7. Collect automated prompts

Use the `snapshot` action to get a list of keywords in the prompt box, looking for the keyword text contained in the `list` or `generic` element.

### 8. Organize the output

Organize the collected keywords into a list format and output them to users.

## Example of Browser Automation Commands

### Launch your browser and access Douyin

```
browser action=start profile=openclaw
browser action=navigate targetUrl=https://www.douyin.com
```

### Get a snapshot of the page (get an element reference)

```
browser action=snapshot refs=aria
```

### Close the login pop-up (if present)

Look for the close button in the pop-up window (usually the `img` or `button` element, near the top-right corner of the pop-up), and click:
```
browser action=act request={"kind":"click","ref"<关闭按钮引用>:""}
```

### Enter keywords in the search bar

```
browser action=act request={"kind":"type","ref":"<搜索栏引用>","text":"<关键词>"}
```

### Wait for the prompt box to load

```
browser action=act request={"kind":"wait","timeMs":2000}
```

### Get the content of the prompt box

```
browser action=snapshot refs=aria
```

## Considerations

1. **Login pop-up processing**: After accessing the Douyin homepage, a login box may pop up, and you need to click the close button (usually the X icon in the upper right corner of the pop-up window) before proceeding.
2. **Login Status**: Some search functions may require login. If you still cannot get the prompt after closing the pop-up window, it is recommended that you manually scan the QR code to log in.
3. **Anti-crawler mechanism**: Douyin may have an anti-crawler mechanism, and you need to add appropriate delays when operating to avoid triggering risk control.
4. **Element References**: Use `refs=aria` to obtain stable element references to ensure operational accuracy.
5. **Waiting Time**: After entering the keyword, wait 1-2 seconds for the automatic prompt box to load.
6. **Mobile adaptation**: Douyin may have different interfaces between mobile and desktop, and it is recommended to use the desktop mode.

## Output Format

```
Keywords: [Entered keywords]
Search suggestions:
1. Suggestion 1
2. Suggestion 2
3. Suggestion 3
...
```