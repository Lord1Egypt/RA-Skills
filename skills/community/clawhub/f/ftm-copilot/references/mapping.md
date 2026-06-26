# Mapping Reference

## ISF Namespace (Critical — always use exactly this)
```
http://www.ibm.com/xmlns/prod/ftm/isf/v3
```
ISF lives at: `OutputLocalEnvironment.PMP.ISF.XMLNSC` in the ACE message tree.

## ISF XML Structure
```xml
<isf:ISFMessage xmlns:isf="http://www.ibm.com/xmlns/prod/ftm/isf/v3"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <isf:Header>
    <isf:BusinessConcept>PAYMENT_ORIGINATION</isf:BusinessConcept>
  </isf:Header>
  <isf:CreditTransfer xsi:type="isf:CreditTransfer">
    <isf:InstructedAmount Currency="USD">1000.00</isf:InstructedAmount>
    <isf:PartyRole xsi:type="isf:DebtorRole">
      <isf:Party><isf:Name>Acme Corp</isf:Name></isf:Party>
    </isf:PartyRole>
    <isf:PartyRole xsi:type="isf:CreditorRole">
      <isf:Party><isf:Name>Supplier Inc</isf:Name></isf:Party>
    </isf:PartyRole>
  </isf:CreditTransfer>
</isf:ISFMessage>
```

## Mapper Framework
| Direction | Framework Nodes |
|---|---|
| External → ISF (inbound) | `BeginMapper` / `EndMapper` |
| ISF → External (outbound) | `BeginOutboundMapper` / `EndOutboundMapper` |

## ESQL Inbound Mapper Template
```esql
BROKER SCHEMA myapp.mapping;
DECLARE ISF_NS NAMESPACE 'http://www.ibm.com/xmlns/prod/ftm/isf/v3';
DECLARE XSI_NS NAMESPACE 'http://www.w3.org/2001/XMLSchema-instance';

CREATE COMPUTE MODULE MyInboundMapper_MapToISF
  CREATE FUNCTION Main() RETURNS BOOLEAN
  BEGIN
    CREATE LASTCHILD OF OutputLocalEnvironment.PMP.ISF AS rRoot NAME 'XMLNSC';
    CREATE LASTCHILD OF rRoot NAMESPACE ISF_NS AS rMsg NAME 'ISFMessage';

    -- CreditTransfer with xsi:type
    CREATE LASTCHILD OF rMsg NAMESPACE ISF_NS AS rCT NAME 'CreditTransfer';
    SET rCT.(XMLNSC.Attribute){XSI_NS}:type = 'isf:CreditTransfer';

    -- Amount with Currency attribute (not child element)
    CREATE LASTCHILD OF rCT NAMESPACE ISF_NS AS rAmt NAME 'InstructedAmount';
    SET rAmt = InputBody.Amount;
    SET rAmt.(XMLNSC.Attribute)Currency = InputBody.Currency;

    -- Debtor party
    CREATE LASTCHILD OF rCT NAMESPACE ISF_NS AS rDebtor NAME 'PartyRole';
    SET rDebtor.(XMLNSC.Attribute){XSI_NS}:type = 'isf:DebtorRole';
    CREATE LASTCHILD OF rDebtor NAMESPACE ISF_NS AS rParty NAME 'Party';
    CREATE LASTCHILD OF rParty NAMESPACE ISF_NS NAME 'Name' VALUE InputBody.OrderingName;

    -- Creditor party
    CREATE LASTCHILD OF rCT NAMESPACE ISF_NS AS rCreditor NAME 'PartyRole';
    SET rCreditor.(XMLNSC.Attribute){XSI_NS}:type = 'isf:CreditorRole';
    CREATE LASTCHILD OF rCreditor NAMESPACE ISF_NS AS rParty2 NAME 'Party';
    CREATE LASTCHILD OF rParty2 NAMESPACE ISF_NS NAME 'Name' VALUE InputBody.BeneficiaryName;

    -- Delete empty optional elements (prevents ISF validation errors)
    IF NOT EXISTS(rCT.{ISF_NS}RemittanceInformation.*[]) THEN
      DELETE FIELD rCT.{ISF_NS}RemittanceInformation;
    END IF;
    RETURN TRUE;
  END;
END MODULE;
```

## Java Compute Node Template
```java
public class MyInboundMapper extends MbJavaComputeNode {
  public void evaluate(MbMessageAssembly inAssembly) throws MbException {
    MbOutputTerminal out = getOutputTerminal("out");
    MbMessage outMessage = new MbMessage(inAssembly.getMessage());
    MbMessageAssembly outAssembly = new MbMessageAssembly(inAssembly, outMessage);
    try {
      // Build ISF at: outMessage.getRootElement() → LocalEnvironment/PMP/ISF/XMLNSC
      out.propagate(outAssembly);
    } finally {
      outMessage.clearMessage();
    }
  }
}
```

## SWIFT Mapping
- **SPN (FxhStandardsProcessing Node)** — converts SWIFT FIN ↔ MTXML
- After SPN, MTXML fields accessible as structured XML in ACE message tree

## Common Pitfalls
- Wrong namespace → all ISF elements fail validation
- Missing `xsi:type` on PartyRole → schema validation failure
- Currency as text content instead of XML attribute → schema failure
- Empty optional elements not deleted → validation error
- Large batch files without chunking in EndMapper → OOM
