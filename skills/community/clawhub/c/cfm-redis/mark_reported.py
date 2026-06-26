#!/usr/bin/env python3
"""Mark message IDs as reported"""
import os

ids = ['bd2eb4fa','d727d910','62a7ee39','17762986','1f285e2b','5f2e4594','07e0e94f','3aa54a00','4c515f21','9977ece1','ba23c32a','04835266','365076ba','18a61385','17762720','48583d34','272c2d37','4268b3f2','360727ea','6e7bada4','07089e23','e641ef5a','ce96d2e9','b3984922','38608e13','43cea28e','082be025','b04b70ed','588c4ac2','435b5c00','df8ff3a4','028655da','a0ca2a77','712f0b3d','e3db9d7e','87cb51f2','d9bfb781','c0a1e4ff','4fd1a684','b2421dc0']
report_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.reported_ids')
with open(report_file, 'a') as f:
    for i in ids:
        f.write(i + '\n')
print(f'Marked {len(ids)} IDs as reported')
