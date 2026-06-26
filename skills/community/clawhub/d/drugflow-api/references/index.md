# DrugFlow Flow Index

## Available Flows
1. `common-apis`
- Call flow: [flows/common-apis/call-flow.md](flows/common-apis/call-flow.md)
- Payload rules: [flows/common-apis/payloads.md](flows/common-apis/payloads.md)
- Shared client: `scripts/common/drugflow_api.py`
- Smoke test: `scripts/common/test_common_apis.py`

2. `virtual-screening`
- Call flow: [flows/virtual-screening/call-flow.md](flows/virtual-screening/call-flow.md)
- Payload rules: [flows/virtual-screening/payloads.md](flows/virtual-screening/payloads.md)
- Script: `scripts/virtual-screening/run_vs_flow.py`

3. `docking`
- Call flow: [flows/docking/call-flow.md](flows/docking/call-flow.md)
- Payload rules: [flows/docking/payloads.md](flows/docking/payloads.md)
- Script: `scripts/docking/run_docking_flow.py`

4. `admet`
- Call flow: [flows/admet/call-flow.md](flows/admet/call-flow.md)
- Payload rules: [flows/admet/payloads.md](flows/admet/payloads.md)
- Script: `scripts/admet/run_admet_flow.py`

5. `molecular-factory`
- Call flow: [flows/molecular-factory/call-flow.md](flows/molecular-factory/call-flow.md)
- Payload rules: [flows/molecular-factory/payloads.md](flows/molecular-factory/payloads.md)
- Script: `scripts/molecular-factory/run_molecular_factory_flow.py`

6. `rescoring`
- Call flow: [flows/rescoring/call-flow.md](flows/rescoring/call-flow.md)
- Payload rules: [flows/rescoring/payloads.md](flows/rescoring/payloads.md)
- Script: `scripts/rescoring/run_rescoring_flow.py`

7. `structure-extract`
- Call flow: [flows/structure-extract/call-flow.md](flows/structure-extract/call-flow.md)
- Payload rules: [flows/structure-extract/payloads.md](flows/structure-extract/payloads.md)
- Script: `scripts/structure-extract/run_structure_extract_flow.py`
- Backend job type: `img2mol`

## Add A New Flow
1. Create `references/flows/<flow>/call-flow.md`.
2. Create `references/flows/<flow>/payloads.md`.
3. Add script(s) to `scripts/<flow>/`.
4. Register the flow in this index and in `SKILL.md`.
