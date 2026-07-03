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
import time    
from pathlib import Path
from cwcommon import apiRequest,manipulateMeta,error,sha256,filePathToDataFile,autoUpdate

if not len(sys.argv)==2:
  error(f"Usage: {sys.argv[0]} <file-path>")

filePath=Path(sys.argv[1])
if not filePath.is_file():
  error(f"File {filePath} is not a plain file.")

autoUpdate()

dataFile=filePathToDataFile(filePath)
docHash=sha256(dataFile)

def verifySeal(meta):
  if "seal" not in meta:
    error("No seal has been found. Please run getseal before verify.")
  respJson=apiRequest("verify",None,{"verifyDocHashes":docHash, "seals": json.dumps(meta["seal"]), "provideInstructions":"true"})
  if not "verifications" in meta:
    meta["verifications"]=[]
  now=int(time.time())
  result=respJson["verificationResults"][0]
  meta["verifications"].append({"result":result, "verifiedAt":now})
  isVerified=result["verified"]
  print(f"seal={json.dumps(result,indent=2)}")
  return isVerified
isVerified=manipulateMeta(filePath,verifySeal)
sys.exit(0 if isVerified else 1)
