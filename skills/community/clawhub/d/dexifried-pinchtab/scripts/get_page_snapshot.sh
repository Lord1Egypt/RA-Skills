#!/bin/bash

URL="http://localhost:9867/snapshot"
TOKEN="b6a91002205211861a1840bc7d1f55e98757ba635436b5a7"

curl -X GET "$URL" \
     -H "Authorization: Bearer $TOKEN"