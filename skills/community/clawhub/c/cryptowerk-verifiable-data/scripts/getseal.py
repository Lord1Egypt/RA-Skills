#!/usr/bin/env python3

'''
Copyright 2026 Cryptowerk Corp.

Licensed under the MIT No Attribution license (MIT-0).
See LICENSE.txt for the full license text.
See DISCLAIMER.md for additional notices regarding use of this Skill with autonomous AI agents.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
'''

import sys
import json
from pathlib import Path
from cwcommon import apiRequest,manipulateMeta,error,autoUpdate

if not len(sys.argv)==2:
  error(f"Usage: {sys.argv[0]} <file-path>")

filePath=Path(sys.argv[1])
if not filePath.is_file():
  error(f"File {filePath} is not a plain file.")

autoUpdate()

def addSeal(meta):
  if "retrievalIds" not in meta or len(meta["retrievalIds"])<=0:
    error("No retrievalId has been found. Please run register before getseal.")
  respJson=apiRequest("getseal",None,{"retrievalId": meta["retrievalIds"][-1]["retrievalId"], "sealFormat":"JSON", "provideVerificationInfos":"true"})
  seal=respJson["documents"][0]["seal"]
  meta["seal"]=seal
  print(f"seal={json.dumps(seal,indent=2)}")
manipulateMeta(filePath,addSeal)
