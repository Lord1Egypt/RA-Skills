---
icon: wave-square
---

# Request Unit (RU)

Different types of RPC queries consume different levels of BlockPI Network resources. Request Unit is a basic charge unit to calculate the usage of the network. This design will provide a fair and transparent experience for every developer and user. The following table shows the RU pricing of each method.&#x20;

If you need to access the data from earlier blocks, you can follow this instruction to turn on the **Archive Mode**, which allows users to access all the historical data of the blockchain.&#x20;

Archive mode will route the requests to archive nodes of the blockchain. It typically takes a **longer time** to process due to the huge amount of data. Since enabling Archive Mode will result in 30% additional RU consumption, we recommend users open Archive Mode only when it’s necessary.

{% hint style="info" %}
Other RPC methods that node client supports but not specified in this table will be charged based on the data size. The rate is 5 RUs per 250 byte.
{% endhint %}

## Additional RU consumption

#### Archive Mode

The resource consumption of an Archive node is significantly higher than that of a full node. Therefore, enabling Archive Mode will result in **30% additional RU consumption**.

#### eth\_getLogs

The eth\_getLogs method is used to request logs from smart contracts, and the amount of data it generates can range from a few KB to several MB. Typically, requests do not exceed 100 KB. For requests that generate a significant amount of data, there will be additional RU consumption. Specifically, when the data volume exceeds 200 KB, it will be calculated by increasing the RU consumption by **100% for every additional 200 KB**.

## Low RU balance reminder

The low RU balance reminder will be triggered when your RU balance drops to 10% of the total maximum RU amount from the RU packages currently available in your account. The system will send you an email as a reminder. This reminder is one-time only, and it will only be triggered again after you purchase a new package.

### Cost Calculator

To calculate the final RPC usage cost, we need to combine the RU table needs and the RU package pricing. Here is a price calculator to estimate the final cost of RPC usage. [https://blockpi.io/pricing/](https://blockpi.io/pricing/)
