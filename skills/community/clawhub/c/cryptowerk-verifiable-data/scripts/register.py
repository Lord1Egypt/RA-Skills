#!/usr/bin/env python3

'''
Copyright 2026 Cryptowerk Corp.

Licensed under the MIT No Attribution license (MIT-0).
See LICENSE.txt for the full license text.
See DISCLAIMER.md for additional notices regarding use of this Skill with autonomous AI agents.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
'''

import sys
import time    
from pathlib import Path
from cwcommon import sha256,apiRequest,manipulateMeta,error,autoUpdate

if not (len(sys.argv)==2 or len(sys.argv)==3):
  error(f"Usage: {sys.argv[0]} <file-path> [lookup-info]")

filePath=Path(sys.argv[1])
if not filePath.is_file():
  error(f"File {filePath} is not a plain file.")

autoUpdate()

lookupInfo=sys.argv[2] if len(sys.argv)>=3 else None

docHash=sha256(filePath)

respJson=apiRequest("register",None,{"hashes": docHash})
#print(respJson)
retrievalId=respJson["documents"][0]["retrievalId"]

def addRetrievalId(meta):
  if not "retrievalIds" in meta:
    meta["retrievalIds"]=[]
  now=int(time.time())
  registration={"retrievalId":retrievalId, "registeredAt":now}
  meta["retrievalIds"].append(registration)
manipulateMeta(filePath,addRetrievalId)

print(f"retrievalId={retrievalId}")
