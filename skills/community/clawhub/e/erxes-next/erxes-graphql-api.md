---
title: erxes GraphQL API – Scope-ийн дагуу үйлдлүүд
description: OAuth token авсны дараа GraphQL mutation/query дуудах бүрэн лавлах
---

# erxes GraphQL API – Scope-ийн дагуу үйлдлүүд

OAuth Device Flow-оор token авсны дараа GraphQL endpoint-г дуудна.  
Нэвтрэлтийн дэлгэрэнгүй: `erxes-app-token-auth.md`

---

## Endpoint

```txt
POST http://localhost:4000/graphql
```

---

## Headers (бүх дуудлагад)

```http
Content-Type: application/json
erxes-subdomain: <subdomain>
Authorization: Bearer <accessToken>
```

---

## Request Format

```json
{
  "query": "<GraphQL mutation эсвэл query string>",
  "variables": { ... }
}
```

---

# Scope-ийн дагуу үйлдлүүд

---

## contacts:read

### customers — Жагсаалт

```graphql
query Customers($page: Int, $perPage: Int, $searchValue: String) {
  customers(page: $page, perPage: $perPage, searchValue: $searchValue) {
    _id
    firstName
    lastName
    primaryEmail
    primaryPhone
    state
    createdAt
  }
}
```

```json
{
  "query": "query Customers($page: Int, $perPage: Int, $searchValue: String) { customers(page: $page, perPage: $perPage, searchValue: $searchValue) { _id firstName lastName primaryEmail primaryPhone state createdAt } }",
  "variables": { "page": 1, "perPage": 20 }
}
```

### customerDetail — Нэгийг дэлгэрэнгүй харах

```graphql
query CustomerDetail($_id: String!) {
  customerDetail(_id: $_id) {
    _id
    firstName
    lastName
    primaryEmail
    primaryPhone
    state
    createdAt
    ownerId
  }
}
```

---

## contacts:create

### customersAdd — Харилцагч үүсгэх

```graphql
mutation CustomersAdd(
  $firstName: String
  $lastName: String
  $primaryEmail: String
  $primaryPhone: String
  $state: String
) {
  customersAdd(
    firstName: $firstName
    lastName: $lastName
    primaryEmail: $primaryEmail
    primaryPhone: $primaryPhone
    state: $state
  ) {
    _id
    firstName
    lastName
    primaryEmail
    primaryPhone
    state
  }
}
```

```json
{
  "query": "mutation CustomersAdd($firstName: String, $lastName: String, $primaryEmail: String, $primaryPhone: String, $state: String) { customersAdd(firstName: $firstName, lastName: $lastName, primaryEmail: $primaryEmail, primaryPhone: $primaryPhone, state: $state) { _id firstName lastName primaryEmail state } }",
  "variables": {
    "firstName": "Бат",
    "lastName": "Болд",
    "primaryEmail": "bat@example.com",
    "primaryPhone": "+97699001122",
    "state": "customer"
  }
}
```

**Response**

```json
{
  "data": {
    "customersAdd": {
      "_id": "abc123...",
      "firstName": "Бат",
      "lastName": "Болд",
      "primaryEmail": "bat@example.com",
      "state": "customer"
    }
  }
}
```

---

## contacts:update

### customersEdit — Мэдээлэл засах

```graphql
mutation CustomersEdit(
  $_id: String!
  $firstName: String
  $lastName: String
  $primaryEmail: String
  $primaryPhone: String
) {
  customersEdit(
    _id: $_id
    firstName: $firstName
    lastName: $lastName
    primaryEmail: $primaryEmail
    primaryPhone: $primaryPhone
  ) {
    _id
    firstName
    lastName
    primaryEmail
    primaryPhone
  }
}
```

```json
{
  "query": "mutation CustomersEdit($_id: String!, $firstName: String, $primaryPhone: String) { customersEdit(_id: $_id, firstName: $firstName, primaryPhone: $primaryPhone) { _id firstName primaryPhone } }",
  "variables": {
    "_id": "abc123...",
    "firstName": "Батаа",
    "primaryPhone": "+97699009900"
  }
}
```

---

## contacts:remove

### customersRemove — Устгах

```graphql
mutation CustomersRemove($customerIds: [String]) {
  customersRemove(customerIds: $customerIds)
}
```

```json
{
  "query": "mutation CustomersRemove($customerIds: [String]) { customersRemove(customerIds: $customerIds) }",
  "variables": {
    "customerIds": ["abc123...", "def456..."]
  }
}
```

---

## contacts:merge

### customersMerge — Нэгтгэх

```graphql
mutation CustomersMerge($customerIds: [String], $customerFields: JSON) {
  customersMerge(customerIds: $customerIds, customerFields: $customerFields) {
    _id
    firstName
    lastName
    primaryEmail
  }
}
```

```json
{
  "query": "mutation CustomersMerge($customerIds: [String], $customerFields: JSON) { customersMerge(customerIds: $customerIds, customerFields: $customerFields) { _id firstName lastName primaryEmail } }",
  "variables": {
    "customerIds": ["abc123...", "def456..."],
    "customerFields": {
      "firstName": "Бат",
      "primaryEmail": "bat@example.com"
    }
  }
}
```

---

## products:read

### products — Жагсаалт

```graphql
query Products($page: Int, $perPage: Int, $searchValue: String) {
  products(page: $page, perPage: $perPage, searchValue: $searchValue) {
    _id
    name
    code
    unitPrice
    type
    categoryId
  }
}
```

---

## products:create

### productsAdd — Бүтээгдэхүүн үүсгэх

```graphql
mutation ProductsAdd(
  $name: String
  $code: String
  $categoryId: String
  $type: String
  $unitPrice: Float
  $uom: String
) {
  productsAdd(
    name: $name
    code: $code
    categoryId: $categoryId
    type: $type
    unitPrice: $unitPrice
    uom: $uom
  ) {
    _id
    name
    code
    unitPrice
  }
}
```

```json
{
  "query": "mutation ProductsAdd($name: String, $code: String, $unitPrice: Float) { productsAdd(name: $name, code: $code, unitPrice: $unitPrice) { _id name code unitPrice } }",
  "variables": {
    "name": "Ус 0.5л",
    "code": "WTR-001",
    "unitPrice": 1500
  }
}
```

---

## products:update

### productsEdit — Засах

```graphql
mutation ProductsEdit($_id: String!, $name: String, $unitPrice: Float) {
  productsEdit(_id: $_id, name: $name, unitPrice: $unitPrice) {
    _id
    name
    unitPrice
  }
}
```

---

## products:remove

### productsRemove — Устгах

```graphql
mutation ProductsRemove($productIds: [String!]) {
  productsRemove(productIds: $productIds)
}
```

---

## products:merge

### productsMerge — Нэгтгэх

```graphql
mutation ProductsMerge($productIds: [String], $productFields: JSON) {
  productsMerge(productIds: $productIds, productFields: $productFields) {
    _id
    name
  }
}
```

---

## products:manage

### productCategoriesAdd — Ангилал үүсгэх

```graphql
mutation ProductCategoriesAdd($name: String!, $code: String, $parentId: String) {
  productCategoriesAdd(name: $name, code: $code, parentId: $parentId) {
    _id
    name
    code
  }
}
```

### uomsAdd — Хэмжих нэгж үүсгэх

```graphql
mutation UomsAdd($name: String!, $code: String!) {
  uomsAdd(name: $name, code: $code) {
    _id
    name
    code
  }
}
```

---

## tags:read

### tags — Жагсаалт

```graphql
query Tags($type: String) {
  tags(type: $type) {
    _id
    name
    type
    colorCode
  }
}
```

---

## tags:create

### tagsAdd — Tag үүсгэх

```graphql
mutation TagsAdd($name: String!, $type: String!, $colorCode: String) {
  tagsAdd(name: $name, type: $type, colorCode: $colorCode) {
    _id
    name
    type
    colorCode
  }
}
```

```json
{
  "query": "mutation TagsAdd($name: String!, $type: String!, $colorCode: String) { tagsAdd(name: $name, type: $type, colorCode: $colorCode) { _id name type } }",
  "variables": {
    "name": "VIP",
    "type": "contacts:customer",
    "colorCode": "#FF0000"
  }
}
```

---

## tags:update

### tagsEdit — Tag засах

```graphql
mutation TagsEdit($_id: String!, $name: String, $colorCode: String) {
  tagsEdit(_id: $_id, name: $name, colorCode: $colorCode) {
    _id
    name
    colorCode
  }
}
```

---

## tags:remove

### tagsRemove — Tag устгах

```graphql
mutation TagsRemove($_id: String!) {
  tagsRemove(_id: $_id)
}
```

---

## tags:tag

### tagsTag — Объектод tag хавсаргах

```graphql
mutation TagsTag($type: String!, $targetIds: [String!]!, $tagIds: [String!]!) {
  tagsTag(type: $type, targetIds: $targetIds, tagIds: $tagIds)
}
```

```json
{
  "query": "mutation TagsTag($type: String!, $targetIds: [String!]!, $tagIds: [String!]!) { tagsTag(type: $type, targetIds: $targetIds, tagIds: $tagIds) }",
  "variables": {
    "type": "contacts:customer",
    "targetIds": ["abc123..."],
    "tagIds": ["tag456..."]
  }
}
```

---

## documents:read

### documents — Жагсаалт

```graphql
query Documents($contentType: String) {
  documents(contentType: $contentType) {
    _id
    name
    contentType
    subType
    code
  }
}
```

---

## documents:create + documents:update

### documentsSave — Үүсгэх / Засах

`_id` өгвөл засах, өгөхгүй бол шинээр үүсгэнэ.

```graphql
mutation DocumentsSave(
  $_id: String
  $name: String!
  $contentType: String
  $content: String
  $code: String
) {
  documentsSave(
    _id: $_id
    name: $name
    contentType: $contentType
    content: $content
    code: $code
  ) {
    _id
    name
    contentType
  }
}
```

---

## documents:remove

### documentsRemove — Устгах

```graphql
mutation DocumentsRemove($_id: String!) {
  documentsRemove(_id: $_id)
}
```

---

## brands:read

### brands — Жагсаалт

```graphql
query Brands {
  brands {
    _id
    name
    description
  }
}
```

---

## brands:create

### brandsAdd — Brand үүсгэх

```graphql
mutation BrandsAdd($name: String!, $description: String) {
  brandsAdd(name: $name, description: $description) {
    _id
    name
    description
  }
}
```

---

## brands:update

### brandsEdit — Brand засах

```graphql
mutation BrandsEdit($_id: String!, $name: String!, $description: String) {
  brandsEdit(_id: $_id, name: $name, description: $description) {
    _id
    name
  }
}
```

---

## brands:remove

### brandsRemove — Устгах

```graphql
mutation BrandsRemove($ids: [String!]) {
  brandsRemove(ids: $ids)
}
```

---

## organization:read

### structures — Байгууллагын бүтэц

```graphql
query Structures {
  structures {
    _id
    title
    departments { _id title }
    branches { _id title }
  }
}
```

---

## organization:manage

### departmentsAdd — Хэлтэс үүсгэх

```graphql
mutation DepartmentsAdd($title: String!, $description: String, $parentId: String) {
  departmentsAdd(title: $title, description: $description, parentId: $parentId) {
    _id
    title
  }
}
```

### branchesAdd — Салбар үүсгэх

```graphql
mutation BranchesAdd($title: String!, $address: String, $parentId: String) {
  branchesAdd(title: $title, address: $address, parentId: $parentId) {
    _id
    title
  }
}
```

---

## teamMembers:read

### users — Гишүүдийн жагсаалт

```graphql
query Users($page: Int, $perPage: Int, $searchValue: String) {
  users(page: $page, perPage: $perPage, searchValue: $searchValue) {
    _id
    email
    username
    details {
      fullName
      position
    }
    isActive
  }
}
```

---

## teamMembers:create

### usersInvite — Шинэ гишүүн урих

```graphql
mutation UsersInvite($entries: [InvitationEntry]) {
  usersInvite(entries: $entries)
}
```

```json
{
  "query": "mutation UsersInvite($entries: [InvitationEntry]) { usersInvite(entries: $entries) }",
  "variables": {
    "entries": [
      { "email": "newmember@example.com", "password": "TempPass123" }
    ]
  }
}
```

---

## teamMembers:update

### usersEdit — Гишүүн засах

```graphql
mutation UsersEdit($_id: String!, $details: UserDetails, $groupIds: [String]) {
  usersEdit(_id: $_id, details: $details, groupIds: $groupIds) {
    _id
    email
    details {
      fullName
      position
    }
  }
}
```

---

## teamMembers:remove

### usersSetActiveStatus — Идэвхгүй болгох

```graphql
mutation UsersSetActiveStatus($_id: String!) {
  usersSetActiveStatus(_id: $_id) {
    _id
    isActive
  }
}
```

---

## automations:read

### automations — Жагсаалт

```graphql
query Automations($page: Int, $perPage: Int) {
  automations(page: $page, perPage: $perPage) {
    _id
    name
    status
    triggers { type }
    actions { type }
  }
}
```

---

## automations:create

### automationsAdd — Автоматжуулалт үүсгэх

```graphql
mutation AutomationsAdd($name: String!, $status: String) {
  automationsAdd(name: $name, status: $status) {
    _id
    name
    status
  }
}
```

```json
{
  "query": "mutation AutomationsAdd($name: String!, $status: String) { automationsAdd(name: $name, status: $status) { _id name status } }",
  "variables": {
    "name": "Шинэ customer мэнд хэлэх",
    "status": "draft"
  }
}
```

---

## automations:update

### automationsEdit — Засах

```graphql
mutation AutomationsEdit($_id: String, $name: String, $status: String) {
  automationsEdit(_id: $_id, name: $name, status: $status) {
    _id
    name
    status
  }
}
```

---

## automations:delete

### automationsRemove — Устгах

```graphql
mutation AutomationsRemove($automationIds: [String]) {
  automationsRemove(automationIds: $automationIds)
}
```

---

# Error Handling

```json
{
  "errors": [
    {
      "message": "Permission denied",
      "path": ["customersAdd"]
    }
  ],
  "data": null
}
```

| Алдаа | Шалтгаан | Үйлдэл |
|-------|---------|--------|
| `Permission denied` | Scope буюу erxes permission дутуу | Хэрэглэгчийн эрх шалгана |
| `Unauthorized` | `accessToken` дууссан эсвэл буруу | Token refresh хийнэ |
| `Not authenticated` | `Authorization` header байхгүй | Header нэмнэ |

> `Unauthorized` гарвал `erxes-app-token-auth.md`-ийн **Алхам 4**-ийг дагана.

---

# Quick Reference

| Scope | Mutation / Query |
|-------|-----------------|
| `contacts:read` | `customers`, `customerDetail` |
| `contacts:create` | `customersAdd` |
| `contacts:update` | `customersEdit` |
| `contacts:remove` | `customersRemove` |
| `contacts:merge` | `customersMerge` |
| `products:read` | `products`, `productDetail` |
| `products:create` | `productsAdd` |
| `products:update` | `productsEdit` |
| `products:remove` | `productsRemove` |
| `products:merge` | `productsMerge` |
| `products:manage` | `productCategoriesAdd/Edit/Remove`, `uomsAdd/Edit/Remove` |
| `tags:read` | `tags` |
| `tags:create` | `tagsAdd` |
| `tags:update` | `tagsEdit` |
| `tags:remove` | `tagsRemove` |
| `tags:tag` | `tagsTag` |
| `documents:read` | `documents` |
| `documents:create` + `documents:update` | `documentsSave` |
| `documents:remove` | `documentsRemove` |
| `brands:read` | `brands` |
| `brands:create` | `brandsAdd` |
| `brands:update` | `brandsEdit` |
| `brands:remove` | `brandsRemove` |
| `organization:read` | `structures`, `departments`, `branches` |
| `organization:manage` | `departmentsAdd/Edit/Remove`, `branchesAdd/Edit/Remove` |
| `teamMembers:read` | `users` |
| `teamMembers:create` | `usersInvite` |
| `teamMembers:update` | `usersEdit` |
| `teamMembers:remove` | `usersSetActiveStatus` |
| `automations:read` | `automations` |
| `automations:create` | `automationsAdd` |
| `automations:update` | `automationsEdit` |
| `automations:delete` | `automationsRemove` |
