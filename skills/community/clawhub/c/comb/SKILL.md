---
name: comb
slug: comb
version: 1.0.0
description: Search 3.2 billion leaked credentials in the COMB dataset via ProxyNova API (no API key required).
homepage: https://www.proxynova.com/tools/comb/
author: ibnaleem
repository: https://github.com/ibnaleem/comb-skill
license: GPL-3.0
changelog: "Initial release"
metadata: {"openclaw":{"requires":{"bins":["curl"]},"os":["linux","darwin","win32"]}}
---

# COMB

One primary service, no API keys needed.

The COMB API allows you to search emails, usernames, and passwords.

Required arg: email, username, or password.

Append `?query=` with the supplied email, username, or password.

Simple request:
```bash
curl 'https://api.proxynova.com/comb?query=jrubin'
# Output:
# {
#    "count": 795,
#    "lines": [
#        "jrubin@247callcapture.com:IUSPgL1T",
#        "jrubin@247callcapture.com:michelle",
#        "jrubin@QandRFS.com:wayne9",
#        "jrubin@absc.net:jake14",
#        "jrubin@absc.net:maomao",
#        "jrubin@academicplanet.com:jacky",
#        "jrubin@acamedicplanet.com:jerry",
#        "jrubin@activevoice.com:jr2203",
#        "jrubin@adsutton.com:jr147369",
#        "jrubin@agtlawyers.com:divorce",
#        "jrubin@agtlawyers.com:divorce1",
#        "jrubin@americanportfolios.com:vizsla123",
#        "jrubin@americaworks.com:hammer316",
#        "jrubin@aol.com:msierk05",
#        "jrubin@apmadvertising.com:sasha2",
#        "jrubin@archideas.com:muaddib16",
#        "jrubin@athensadmin.com:stab8ler",
#        "jrubin@atsautomation.com:slower",
#        "jrubin@bcps.org:lacrosse",
#        "jrubin@bear.com:pizza99"
#    ]
# }
```

## Rate Limits
The API will only return 100 results max. The API will also limit you to about 100 requests per minute.

## References
https://www.proxynova.com/tools/comb/
https://cybernews.com/news/largest-compilation-of-emails-and-passwords-leaked-free/