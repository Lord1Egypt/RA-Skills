# FakeX-Till-YouAI
FakeX-Till-YouAI helps AI beginners learn in public by turning daily AI digests into thoughtful X post drafts. Borrowing the spirit of “fake it till you make it,” it encourages users to post before they feel fully ready, sharpen their thinking through output, and grow an AI IP as confidence catches up with curiosity.

## Inspiration

This project was inspired by Zara Zhang’s digest workflow and especially her `follow-builders` skill. (https://github.com/zarazhangrui/follow-builders)

Many thanks to Zara for building and sharing a digest system that makes this downstream workflow possible.

## What this skill does

This skill handles the posting layer after a digest is generated.

It helps users:

- turn a daily AI digest into post drafts
- shape drafts around their AI IP positioning
- choose the drafts they like
- publish manually or automatically to X
- schedule selected posts at custom times

## Important

This skill is **not** a standalone digest generator.

It needs to be used **together with a digest source** in order to fully work.

It can work with many kinds of daily digests, but it is **strongly recommended** to use it together with Zara Zhang’s `follow-builders` skill.

## Intended workflow

1. A digest is generated
2. FakeX-Till-YouAI turns that digest into post drafts
3. The user selects any number of drafts
4. The user chooses posting times
5. Posts are either:
   - published automatically to X, or
   - handed back to the user for manual posting

## Modes

### Full automatic
The agent publishes directly to X using the user’s own X API credentials.

### Half automatic
The agent only generates final post copy. The user copies and posts manually.

## Features

- onboarding for AI IP positioning
- onboarding for preferred post style
- onboarding for reference accounts
- source-aware draft generation
- rotating source placement styles
- flexible draft selection
- flexible scheduling

## Requirements

- a daily digest source
- strongly recommended: Zara Zhang’s `follow-builders` skill (https://github.com/zarazhangrui/follow-builders)
- X API credentials if using full automatic mode

## Notes

This project does **not** include or ship any user API credentials.

Users must provide their own X API credentials if they want automatic posting.

## License

MIT
