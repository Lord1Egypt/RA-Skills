#!/bin/bash

URL="http://localhost:9867/launch"
TOKEN="b6a91002205211861a1840bc7d1f55e98757ba635436b5a7"

curl -X POST "$URL" \
     -H "Authorization: Bearer $TOKEN"