# RSS Feed Format Reference

## Feed Template

```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" 
  xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"
  xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>Your Podcast Name</title>
    <link>https://your-domain.com</link>
    <language>en</language>
    <description>Your podcast description</description>
    <itunes:owner>
      <itunes:name>Your Name</itunes:name>
      <itunes:email>your@email.com</itunes:email>
    </itunes:owner>
    <itunes:author>Host A &amp; Host B</itunes:author>
    <itunes:summary>Short summary</itunes:summary>
    <itunes:category text="Technology"/>
    <itunes:explicit>false</itunes:explicit>
    <itunes:image href="https://your-domain.com/cover.jpg"/>
    <lastBuildDate>RFC 2822 date</lastBuildDate>

    <item>
      <title>EP001 | Episode Title</title>
      <description>Episode description</description>
      <enclosure url="https://your-domain.com/episodes/YYYY-MM-DD-ep001.mp3" length="ACTUAL_BYTES" type="audio/mpeg"/>
      <pubDate>Tue, 03 Mar 2026 08:00:00 +0000</pubDate>
      <itunes:duration>MM:SS</itunes:duration>
      <itunes:summary>Episode description</itunes:summary>
      <itunes:image href="https://your-domain.com/cover.jpg"/>
      <guid isPermaLink="false">your-podcast-YYYY-MM-DD-ep001</guid>
    </item>
  </channel>
</rss>
```

## Key Rules

- Newest episodes first
- `<guid>` unique per episode, `isPermaLink="false"`
- `<enclosure length>` = **actual file size** in bytes
- `<itunes:duration>` = **actual audio duration** via ffprobe
- `<itunes:owner>` with email required for Apple/Spotify
- Cover image: 3000x3000 JPEG minimum
- `<pubDate>` in RFC 2822 format
